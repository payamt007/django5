from base.models import Feed, Post
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def create_post(item, feed: Feed):
    old_post = Post.objects.filter(link=item.link, feed=feed)
    if old_post:
        logger.info(f"repeated post for {feed.title}!")
        return
    new_post = Post()
    new_post.title = item.title
    if hasattr(item, "link"):
        new_post.link = item.link
    if hasattr(item, "description"):
        new_post.description = item.description
    if hasattr(item, "pubDate"):
        new_post.pubDate = item.pubDate
    new_post.feed = feed
    new_post.save()
    logger.info(f"saved {new_post} in db!")
