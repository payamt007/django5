from rss_parser.views import PostViewSet
from rss_parser.models import Feed, Post
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.test import APIClient


class PostViewSetTest(APITestCase):
    def setUp(self) -> None:
        self.view = PostViewSet.as_view({'get': 'list', 'patch': 'update'})
        user = User.objects.create_user(username="test", password="test")
        self.feed = Feed.objects.create(
            title='Test Feed', link='https://example.com/feed/', user=user)
        self.post = Post.objects.create(feed=self.feed, title='Test Post', link='https://example.com/post/',
                                        description='Test description')
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    """ def test_list_posts(self) -> None:
        response = self.client.get('/api/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1) """

    def test_update_post(self) -> None:
        response = self.client.patch(
            f'/api/posts/{self.post.pk}/', data={'read': True})
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertTrue(self.post.read)

    def test_update_post_invalid_data(self) -> None:
        self.client.patch(
            f'/api/posts/{self.post.pk}/', data={'invalid_field': True})
        self.post.refresh_from_db()
        self.assertFalse(hasattr(self.post, 'invalid_field'))


class PostFilterAPIViewTest(APITestCase):
    def setUp(self) -> None:
        self.post1 = Post.objects.create(
            title='Test Post 1', read=True, followed=True)
        self.post2 = Post.objects.create(
            title='Test Post 2', read=False, followed=True)
        self.post3 = Post.objects.create(
            title='Test Post 3', read=True, followed=False)
        self.post4 = Post.objects.create(
            title='Test Post 4', read=True, followed=True)
        user = User.objects.create_user(username="test", password="test")
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_filter_posts(self) -> None:
        response = self.client.get(
            '/api/filter-posts?read=true&followed=true&order_by=pubDate')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # print("response", response.data)
        self.assertEqual(response.data[0]['title'], 'Test Post 1')

    def test_filter_posts_invalid_params(self) -> None:
        response = self.client.get('/api/filter-posts', {'invalid_param': 'value'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_posts_missing_required_params(self) -> None:
        response = self.client.get('/api/filter-posts')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
