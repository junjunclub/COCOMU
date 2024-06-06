from rest_framework import serializers
from .models import Article, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "nickname",
        )


# 댓글 serializer
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("user", "content", "created_at", "updated_at", "article","pk",)
        read_only_fields = ("user", "article")


# 전체 게시글 serializer
class ArticleListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Article
        fields = ("title", "created_at", "category", "user", "pk")


# 상세 게시글 serializer
class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = (
            "title",
            "content",
            "rate",
            "created_at",
            "updated_at",
            "category",
            "movie",
            "user",
            "comments",
            "pk",
        )
        # all_auth때문에 넣은 것
        read_only_fields = ("user",)

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title','content','user',)