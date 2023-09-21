from django.test import TestCase
from unittest.mock import patch, MagicMock
from rss_parser.models import Feed
from rss_parser.tasks import read_feed_links, parse_feed_item
from django.contrib.auth.models import User
from django.conf import settings


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

    @patch('rss_parser.tasks.cache')
    @patch('rss_parser.tasks.parse_feed_item.apply_async')
    @patch('rss_parser.tasks.feedparser.parse')
    def test_read_feed_links_first_exception(self, feed_parser: MagicMock, parse_feed_item_mock: MagicMock,
                                             mock_cache: MagicMock) -> None:
        """
        Test triggering back-off mechanism in case of first exception
        """

        mock_cache.set.return_Value = None
        # Mock the feedparser.parse function to raise an exception
        feed_parser.side_effect = Exception('Boom!')

        # Call the task
        parse_feed_item(self.feed.id)

        # Ensure that the feed fails counter is incremented
        self.feed.refresh_from_db()
        parse_feed_item_mock.return_value = None

        self.assertEqual(self.feed.fails, 1)

        countdown = settings.FEED_READER["FEED_READER_RETRY_TIME"]
        parse_feed_item_mock.assert_called_once_with(args=[self.feed.id, True], countdown=countdown)
