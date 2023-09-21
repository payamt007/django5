import datetime

from django.test import TestCase
from unittest.mock import patch, MagicMock
from rss_parser.models import Feed, Post
from rss_parser.tasks import read_feed_links, parse_feed_item
from django.contrib.auth.models import User
from django.conf import settings
from .heper import SampleEntryClass


class FeedReaderTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username="test", password="test")
        self.feed = Feed.objects.create(title="sample0", link='https://example.com/feed', user=user)

    @patch('rss_parser.tasks.parse_feed_item.apply_async')
    def test_read_feed_links_normally(self, mock_parse_feed_item: MagicMock) -> None:
        """
        Test if feed parsed normally in case of normal operation without any exceptions
        """
        mock_parse_feed_item.return_value = True

        read_feed_links()

        mock_parse_feed_item.assert_called_once_with(args=[self.feed.id])

    @patch('rss_parser.tasks.parse_feed_item.apply_async')
    @patch('rss_parser.tasks.feedparser.parse')
    def test_read_feed_links_first_exception(self, feed_parser: MagicMock, parse_feed_item_mock: MagicMock) -> None:
        """
        Test triggering back-off mechanism in case of first exception
        """

        # Mock the feedparser.parse function to raise an exception
        feed_parser.side_effect = Exception('Boom!')

        parse_feed_item(self.feed.id)

        # Ensure that the feed fails counter is incremented
        self.feed.refresh_from_db()
        self.assertEqual(self.feed.fails, 1)

        parse_feed_item_mock.return_value = None
        countdown = settings.FEED_READER["FEED_READER_RETRY_TIME"]
        parse_feed_item_mock.assert_called_once_with(args=[self.feed.id, True], countdown=countdown)

    @patch('rss_parser.tasks.cache')
    @patch('rss_parser.tasks.feedparser.parse')
    def test_save_feed_links(self, feed_parser: MagicMock, fake_cache: MagicMock):
        fake_cache.get.return_value = None
        fake_cache.set.return_value = None

        feed_parser.return_value.entries = [SampleEntryClass(
            title='sample', link='https://example.com/feed', description='some notes...')]
        current_time = datetime.datetime.now()
        feed_parser.return_value.feed.updated = current_time

        parse_feed_item(self.feed.id)

        saved_post_count = Post.objects.filter(link='https://example.com/feed', feed__id=self.feed.id).count()

        self.assertEqual(saved_post_count, 1)
        fake_cache.set.assert_called_once_with(f"last_feed_update_time_{self.feed.id}", current_time)
