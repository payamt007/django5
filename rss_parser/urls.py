from django.urls import include, path
from rest_framework import routers

from rss_parser.views import (FeedViewSet, ForceRefreshAPIview,
                              PostFilterAPIView, PostViewSet)

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"feeds", FeedViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("force-refresh-feed", ForceRefreshAPIview.as_view()),
    path("filter-posts", PostFilterAPIView.as_view()),
]
