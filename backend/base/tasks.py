import feedparser
from celery import shared_task
from base.models import Feed, Post
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
        parse_feed_item.apply_async(args=[feed.link, feed.id])


@shared_task
def retry_failed_feed(id: int) -> None:
    """
    This is the background process that is runned when a feed encountered errors
    """
    feed = Feed.objects.get(id=id)
    max_exceptions = settings.FEED_READER["MAX_FEED_READER_ERRORS"]
    countdown = settings.FEED_READER["FEED_READER_RETRY_TIME"]
    try:
        feed_content = feedparser.parse(feed.link)
        save_feed_items(feed_content, feed)
        feed.fails = 0
        feed.save()
    except Exception as e:
        logger.error(f"Failed retrying {feed.link} --> {e}")
        if feed.fails == max_exceptions:
            feed.stopped = True
            feed.fails = 0
            feed.save()
        else:
            feed.fails = feed.fails + 1
            feed.save()
            retry_failed_feeds.apply_async(args=[feed.id], countdown=countdown)


@shared_task
def parse_feed_item(feed_link: str, feed_id: int):
    try:
        feed_content = feedparser.parse(feed_link)
        last_feed_update_time = cache.get(f"last_feed_update_time_{feed_id}", None)
        if hasattr(feed_content.feed, "updated") and last_feed_update_time == str(feed_content.feed.updated):
            return
        else:
            for item in feed_content.entries:
                save_post(item, feed_id)
            if hasattr(feed_content.feed, "updated"):
                cache.set(f"last_feed_update_time_{feed_id}", feed_content.feed.updated)
    except Exception as e:
        logger.error(f"Failed paring {feed_link} --> {e}")
        feed = Feed.objects.get(id=id)
        feed.fails = feed.fails + 1
        feed.save()
        retry_failed_feed.apply_async(args=[feed_id], countdown=120)
