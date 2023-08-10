import feedparser
from celery import shared_task
from base.models import Feed, Post
from django.core.cache import cache
from django.conf import settings


@shared_task
def read_feed_links() -> None:
    """
    This is the base background process that is runned by
    celery beat scheduler to get feeds from sources
    """
    feeds = Feed.objects.filter(stopped=False, followed=True, fails=0)
    for feed in feeds:
        try:
            feed_conetnt = feedparser.parse(feed.link)
            save_feed_items(feed_conetnt, feed)
        except Exception:
            feed.fails = feed.fails + 1
            feed.save()
            retry_failed_feeds.apply_async(args=[feed.id], countdown=120)


@shared_task
def retry_failed_feeds(id: int) -> None:
    """
    This is the background process that is runned when a feed encountered errors
    """
    feed = Feed.objects.get(id=id)
    max_exceptions = settings.MAX_FEED_READER_ERRORS
    countdown = settings.FEED_READER_RETRY_TIME
    try:
        feed_conetnt = feedparser.parse(feed.link)
        save_feed_items(feed_conetnt, feed)
        feed.fails = 0
        feed.save()
    except Exception:
        if feed.fails == max_exceptions:
            feed.stopped = True
            feed.fails = 0
            feed.save()
        else:
            feed.fails = feed.fails + 1
            feed.save()
            retry_failed_feeds.apply_async(args=[feed.id], countdown=countdown)


def save_feed_items(feed_conetnt, feed) -> bool:
    last_feed_update_time = cache.get(f"last_feed_update_time_{feed.id}", 0)
    if last_feed_update_time == str(feed_conetnt.modified):
        return True
    else:
        cache.set(f"last_feed_update_time_{feed.id}", feed_conetnt.modified)
        for item in feed_conetnt.entries:
            old_post = Post.objects.filter(link=item.link).first()
            if not old_post:
                new_post = Post()
                new_post.title = item.title
                new_post.link = item.link
                new_post.description = item.description
                if hasattr(item, 'pubDate'):
                    new_post.pubDate = item.pubDate
                new_post.feed = feed
                new_post.save()
        return False
