from django.test import TestCase
from unittest.mock import patch, MagicMock
from rss_parser.models import Feed
from rss_parser.tasks import read_feed_links
from django.contrib.auth.models import User


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

# @patch('base.tasks.retry_failed_feeds.apply_async')
# @patch('base.tasks.feedparser.parse')
# def test_read_feed_links_first_exception(self, mock_parse: MagicMock, mock_retry_failed_feeds: MagicMock) -> None:
#     """
#     Test triggering back-off mechanism in case of first exception
#     """
#
#     # Mock the feedparser.parse function to raise an exception
#     mock_parse.side_effect = Exception('Boom!')
#
#     # Call the task
#     read_feed_links()
#
#     # Ensure that the feed fails counter is incremented
#     self.feed.refresh_from_db()
#
#     self.assertEqual(self.feed.fails, 1)
#
#     # Ensure that retry_failed_feeds.apply_async is called
#     mock_retry_failed_feeds.assert_called_once_with(self.feed.id, countdown=120)
