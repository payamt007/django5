from rest_framework import serializers
from base.models import Post, Feed


class UpdatePostSerializer(serializers.ModelSerializer[Post]):

    class Meta:
        model = Post
        fields = ('readed', 'followed',)


class PostSerializer(serializers.ModelSerializer[Post]):

    class Meta:
        model = Post
        fields = '__all__'


class FeedSerializer(serializers.ModelSerializer[Feed]):

    class Meta:
        model = Feed
        fields = ('title', 'link', 'followed',)


class ForceRefreshSerializer(serializers.Serializer[str]):

    id = serializers.IntegerField()


class FilterSerializer(serializers.Serializer):

    feed = serializers.IntegerField(required=False)
    readed = serializers.BooleanField(required=False)
    followed = serializers.BooleanField(required=False)
    order_by = serializers.ChoiceField(['pubDate', '-pubDate'], required=True)
