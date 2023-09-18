from django.test import TestCase
from unittest.mock import patch, MagicMock
from base.models import Feed
from base.tasks import read_feed_links


class FeedReaderTestCase(TestCase):
    def setUp(self) -> None:
        self.feed = Feed.objects.create(
            link='http://example.com/feed', stopped=False, fails=0)

    @patch('base.tasks.save_feed_items')
    @patch('base.tasks.feedparser.parse')
    def test_read_feed_links_normally(self, mock_parse: MagicMock, mock_save_feed_items: MagicMock) -> None:
        """
        Test if feed parsed normally in case of normal operation without any exceptions
        """

        sample_parsed_content = object
        mock_parse.return_value = sample_parsed_content
        mock_save_feed_items.return_value = True

        read_feed_links()

        mock_save_feed_items.assert_called_once_with(
            sample_parsed_content, self.feed)

    @patch('base.tasks.retry_failed_feeds.apply_async')
    @patch('base.tasks.feedparser.parse')
    def test_read_feed_links_first_exception(self, mock_parse: MagicMock, mock_retry_failed_feeds: MagicMock) -> None:
        """
        Test triggering back-off mechanism in case of first exception
        """

        # Mock the feedparser.parse function to raise an exception
        mock_parse.side_effect = Exception('Boom!')

        # Call the task
        read_feed_links()

        # Ensure that the feed fails counter is incremented
        self.feed.refresh_from_db()

        self.assertEqual(self.feed.fails, 1)

        # Ensure that retry_failed_feeds.apply_async is called
        mock_retry_failed_feeds.assert_called_once_with(self.feed.id, countdown=120)
