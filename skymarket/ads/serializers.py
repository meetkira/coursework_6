from rest_framework import serializers

from ads.models import Comment, Ad
from users.models import User


class CommentSerializer(serializers.ModelSerializer):
    author_first_name = serializers.CharField(max_length=255, source="author.first_name")
    author_last_name = serializers.CharField(max_length=255, source="author.last_name")

    class Meta:
        model = Comment
        fields = ["pk", "text", "author_id", "ad_id", "author_first_name", "author_last_name", "created_at"]


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ["pk", "title", "price", "description", "image"]


class AdCreateSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(required=False)
    phone = serializers.CharField(required=False, source="author.phone")
    author_first_name = serializers.CharField(max_length=255, required=False, source="author.first_name")
    author_last_name = serializers.CharField(max_length=255, required=False, source="author.last_name")
    author = serializers.SlugRelatedField(
        required=True,
        queryset=User.objects.all(),
        slug_field='id'
    )

    class Meta:
        model = Ad
        fields = ["pk", "title", "price", "description", "author", "phone", "author_first_name", "author_last_name"]


class AdDetailSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source="author.phone")
    author_first_name = serializers.CharField(max_length=255, source="author.first_name")
    author_last_name = serializers.CharField(max_length=255, source="author.last_name")

    class Meta:
        model = Ad
        fields = ["pk", "title", "price", "description", "author_id", "phone", "author_first_name", "author_last_name",
                  "image"]
