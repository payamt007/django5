from django.test import TestCase
from unittest.mock import patch, MagicMock
from base.models import Feed, Post
from base.tasks import retry_failed_feeds, save_feed_items


class RetryFaildTasksFirstTimeTestCase(TestCase):

    def setUp(self) -> None:
        self.feed = Feed.objects.create(
            link='http://example.com/feed', stopped=False, fails=1)

    @patch('base.tasks.retry_failed_feeds.apply_async')
    @patch('base.tasks.feedparser.parse')
    def test_retry_failed_first_time_exception(self, mock_parse: MagicMock, mock_retry_failed_feeds: MagicMock) -> None:

        mock_parse.side_effect = Exception

        retry_failed_feeds(self.feed.id)

        self.feed.refresh_from_db()

        self.assertEqual(self.feed.fails, 2)
        mock_retry_failed_feeds.assert_called_once_with(self.feed.id, countdown=300)


class RetryFaildTasksSecondTimeTestCase(TestCase):

    def setUp(self) -> None:
        self.feed = Feed.objects.create(
            link='http://example.com/feed', stopped=False, fails=2)

    @patch('base.tasks.retry_failed_feeds.apply_async')
    @patch('base.tasks.feedparser.parse')
    def test_retry_failed_second_time_exception(self, mock_parse: MagicMock, mock_retry_failed_feeds: MagicMock) -> None:

        mock_parse.side_effect = Exception

        retry_failed_feeds(self.feed.id)

        self.feed.refresh_from_db()

        self.assertEqual(self.feed.fails, 3)
        mock_retry_failed_feeds.assert_called_once_with(self.feed.id, countdown=480)


class RetryFaildTasksThirdTimeTestCase(TestCase):

    def setUp(self) -> None:
        self.feed = Feed.objects.create(
            link='http://example.com/feed', stopped=False, fails=3)

    @patch('base.tasks.feedparser.parse')
    def test_retry_failed_third_time_exception(self, mock_parse: MagicMock) -> None:

        mock_parse.side_effect = Exception

        retry_failed_feeds(self.feed.id)

        self.feed.refresh_from_db()
        self.assertEqual(self.feed.fails, 0)
        self.assertEqual(self.feed.stopped, True)


class SaveFeedItemsTestCase(TestCase):

    def setUp(self) -> None:
        self.feed = Feed.objects.create(
            link='http://example.com/feed', stopped=False, fails=1)
        self.Post = Post.objects.create(
            title='old post title', description='some desc...', link='http://oldexample.com/feed')

    @patch('base.tasks.cache.get')
    @patch('base.tasks.cache.set')
    def test_save_new_post(self, mock_cache_set: MagicMock, mock_cache_get: MagicMock) -> None:
        mock_cache_get.return_value = 0
        mock_cache_set.return_value = True
        feed_conetnt = MagicMock()
        feed_conetnt.modified = "2021"

        class SampleEntryClass:
            def __init__(self, title: str, link: str, description: str) -> None:
                self.title = title
                self.link = link
                self.description = description
        feed_conetnt.entries = [SampleEntryClass(
            title='sample', link='http://example.com/feed', description='some notes...')]

        save_feed_items(feed_conetnt, self.feed)

        saved_post_count = Post.objects.filter(link='http://example.com/feed').count()

        self.assertEqual(saved_post_count, 1)

    @patch('base.tasks.cache.get')
    @patch('base.tasks.cache.set')
    def test_dont_save_old_post(self, mock_cache_set: MagicMock, mock_cache_get: MagicMock) -> None:
        mock_cache_get.return_value = 0
        mock_cache_set.return_value = True
        feed_conetnt = MagicMock()
        feed_conetnt.modified = "2021"

        class SampleEntryClass:
            def __init__(self, title: str, link: str, description: str) -> None:
                self.title = title
                self.link = link
                self.description = description

        feed_conetnt.entries = [SampleEntryClass(
            title='old post title', link='http://oldexample.com/feed', description='some desc...')]

        save_feed_items(feed_conetnt, self.feed)

        saved_post_count = Post.objects.filter(
            link='http://oldexample.com/feed').count()

        self.assertEqual(saved_post_count, 1)

    @patch('base.tasks.cache.get')
    def test_cache_working_correctly(self, mock_cache_get: MagicMock) -> None:
        mock_cache_get.return_value = "2021"
        feed_conetnt = MagicMock()
        feed_conetnt.modified = "2021"

        response = save_feed_items(feed_conetnt, self.feed)

        self.assertEqual(response, True)
