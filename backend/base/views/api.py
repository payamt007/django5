import feedparser
from rest_framework import viewsets
from rest_framework import mixins
from base.models import Post, Feed
from base.serializers import (
    PostSerializer,
    CreateOrUpdateFeedSerializer,
    FeedSerializer,
    FeedDeleteSerializer,
    FilterSerializer,
    ForceRefreshSerializer,
    UpdatePostSerializer,
)
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from helper import save_post
from base.permissions import IsOwner


class PostViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    Viewset for handling updating (reading, following) posts
    """

    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer


class FeedViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """
    Viewset for handling creating, listing and
    updating (unfollowing, following) rss feeds
    """

    queryset = Feed.objects.all()
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Feed.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return CreateOrUpdateFeedSerializer
        else:
            return FeedSerializer

    @extend_schema(request=CreateOrUpdateFeedSerializer, summary="Insert a new Feed")
    def create(self, request, *args, **kwargs) -> Response:
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(summary="Retrieve a list of Feeds")
    def list(self, request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @extend_schema(
        description="""Update a Feed , followed to true or false
                        , Or maybe change title or url"""
    )
    def update(self, request, *args, **kwargs) -> Response:
        return super().update(request, *args, **kwargs)


class PostFilterAPIView(APIView):
    """
    APIView for filtering the posts
    """

    allowed_methods = ["get"]
    serializer_class = PostSerializer
    permission_classes = [IsOwner]

    @extend_schema(summary="Filter posts", parameters=[FilterSerializer])
    def get(self, request):
        query_params = request.GET.copy()
        serializer = FilterSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        order_by_param = serializer.validated_data.pop("order_by")
        filtered_results = Post.objects.filter(**serializer.validated_data).order_by(
            order_by_param
        )
        # filtered_results = Post.objects.order_by(order_by_param[0])
        result_serializer = PostSerializer(filtered_results, many=True)

        return Response(data=result_serializer.data, status=status.HTTP_200_OK)


class ForceRefreshAPIview(APIView):
    """
    APIView for refreshing status of failed feeds
    """

    allowed_methods = ["post"]
    permission_classes = [IsOwner]

    @extend_schema(request=ForceRefreshSerializer)
    def post(self, request) -> Response:
        serializer = ForceRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id = serializer.validated_data["id"]
        feed = Feed.objects.get(id=id)

        try:
            feed_content = feedparser.parse(feed.link)
            for item in feed_content.entries:
                old_post = Post.objects.filter(link=item.link).first()
                if not old_post:
                    save_post(item, feed)
            feed.fails = 0
            feed.stopped = False
            feed.save()
            return Response(
                data={
                    "message": "Feed refresh Success! Feed returned to normal scrapping schedule!"
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                data={"message": "Feed refresh Failed! Sorry!"},
                status=status.HTTP_406_NOT_ACCEPTABLE,
            )
