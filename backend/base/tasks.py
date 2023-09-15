import feedparser
from celery import shared_task
from base.models import Feed, Post
from django.core.cache import cache
from django.conf import settings
from celery.utils.log import get_task_logger
from helper import create_post

logger = get_task_logger(__name__)


@shared_task
def read_feed_links() -> None:
    """
    This is the base background process that is run by
    celery beat scheduler to get feeds from sources
    """
    feeds = Feed.objects.filter(stopped=False, followed=True, fails=0)
    logger.info(f'Feed paring task start for {feeds}')
    for feed in feeds:
        try:
            feed_content = feedparser.parse(feed.link)
            save_feed_items(feed_content, feed)
            logger.info(f'parsed feed content of : {feed.link}')
        except Exception as e:
            logger.error(f"Failed paring {feed.link} --> {e}")
            feed.fails = feed.fails + 1
            feed.save()
            retry_failed_feeds.apply_async(args=[feed.id], countdown=120)
    logger.info('Feed paring task finished...')


@shared_task
def retry_failed_feeds(id: int) -> None:
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


def save_feed_items(feed_content, feed):
    last_feed_update_time = cache.get(f"last_feed_update_time_{feed.id}", 0)
    if hasattr(feed_content, "modified") and last_feed_update_time == str(feed_content.modified):
        return
    else:
        for item in feed_content.entries:
            # old_post = Post.objects.filter(link=item.link).first()
            # if not old_post:
            create_post(item, feed)
        if hasattr(feed_content, "modified"):
            cache.set(f"last_feed_update_time_{feed.id}", feed_content.modified)
