from base.models import Feed, Post
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)


def save_post(item, feed_id: int):
    old_post = Post.objects.filter(link=item.link, feed__id=feed_id)
    logger.info(f"old_post for {item} {feed_id} : {old_post.first()}!")
    if old_post:
        logger.info(f"repeated post for {feed_id} feed!")
        return
    new_post = Post()
    new_post.title = item.title
    if hasattr(item, "link"):
        new_post.link = item.link
    if hasattr(item, "description"):
        new_post.description = item.description
    if hasattr(item, "pubDate"):
        new_post.pubDate = item.pubDate
    feed = Feed.objects.get(id=feed_id)
    new_post.feed = feed
    new_post.save()
    logger.info(f"saved {new_post} in db!")
