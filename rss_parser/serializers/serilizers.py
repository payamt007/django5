from rest_framework import serializers
from rss_parser.models import Post, Feed


class UpdatePostSerializer(serializers.ModelSerializer[Post]):
    class Meta:
        model = Post
        fields = (
            "readed",
            "followed",
        )


class PostSerializer(serializers.ModelSerializer[Post]):
    class Meta:
        model = Post
        fields = "__all__"


class CreateOrUpdateFeedSerializer(serializers.ModelSerializer[Feed]):
    key = serializers.SerializerMethodField()

    def get_key(self, obj):
        return obj.id

    class Meta:
        model = Feed
        fields = (
            "id",
            "key",
            "title",
            "link",
        )


class FeedSerializer(serializers.ModelSerializer[Feed]):
    key = serializers.SerializerMethodField()

    def get_key(self, obj):
        return obj.id

    class Meta:
        model = Feed
        fields = (
            "id",
            "key",
            "title",
            "link",
            "followed",
            "stopped",
        )


class FeedDeleteSerializer(serializers.Serializer):
    keys = serializers.ListField()


class ForceRefreshSerializer(serializers.Serializer[str]):
    id = serializers.IntegerField()

    def validate_id(self, value: int):
        try:
            Feed.objects.get(id=value)
            return value
        except Feed.DoesNotExist:
            raise serializers.ValidationError("No such Feed id!")


class FilterSerializer(serializers.Serializer):
    feed = serializers.IntegerField(required=False)
    readed = serializers.BooleanField(required=False)
    followed = serializers.BooleanField(required=False)
    order_by = serializers.ChoiceField(["pubDate", "-pubDate"], required=True)
