import feedparser
from celery import shared_task
from rss_parser.models import Feed
from django.core.cache import cache
from django.conf import settings
from celery.utils.log import get_task_logger
from helper import save_post

logger = get_task_logger(__name__)


@shared_task
def read_feed_links() -> None:
    feeds = Feed.objects.filter(stopped=False, followed=True, fails=0)
    logger.info(f'Feed paring task start for {feeds}')
    for feed in feeds:
        parse_feed_item.apply_async(args=[feed.id])


@shared_task
def parse_feed_item(feed_id: int, retry: bool = False):
    feed = Feed.objects.get(id=feed_id)
    try:
        # if feed.title == "tasnim0":
        #     raise Exception("Chelen Balam Shetted!")
        feed_content = feedparser.parse(feed.link)
        last_feed_update_time = cache.get(f"last_feed_update_time_{feed_id}", None)
        if hasattr(feed_content.feed, "updated") and last_feed_update_time == str(feed_content.feed.updated):
            return
        else:
            for item in feed_content.entries:
                save_post(item, feed)
            if retry:
                feed.fails = 0
                feed.stopped = False
                feed.save()
            if hasattr(feed_content.feed, "updated"):
                cache.set(f"last_feed_update_time_{feed_id}", feed_content.feed.updated)
            return True
    except Exception as e:
        max_exceptions = settings.FEED_READER["MAX_FEED_READER_ERRORS"]
        countdown = settings.FEED_READER["FEED_READER_RETRY_TIME"]
        if feed.fails == max_exceptions:
            feed.stopped = True
            feed.fails = 0
            feed.save()
        else:
            logger.error(f"Failed paring {feed.link} --> {e}")
            feed.fails = feed.fails + 1
            feed.save()
            parse_feed_item.apply_async(args=[feed_id, True], countdown=countdown)
