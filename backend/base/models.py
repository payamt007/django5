from django.db import models


class Feed(models.Model):

    title = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    followed = models.BooleanField(default=True)
    stopped = models.BooleanField(default=False)
    fails = models.SmallIntegerField(default=0)


class Post(models.Model):

    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    link = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    readed = models.BooleanField(default=False)
    followed = models.BooleanField(default=False)
    pubDate = models.DateTimeField(auto_now=True)

