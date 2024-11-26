from __future__ import annotations

from django.contrib.auth.views import get_user_model
from rest_framework import serializers

from .models import Snippet, User


class SnippetListSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    password = serializers.CharField(write_only=True, allow_blank=True)
    linenos = serializers.BooleanField(write_only=True)
    view_once = serializers.BooleanField(write_only=True)

    class Meta:
        model = Snippet
        fields = [
            "url",
            "author",
            "category",
            "title",
            "linenos",
            "code",
            "language_choices",
            "style_choices",
            "view_once",
            "snippet_expiration",
            "password",
        ]
        extra_kwargs = {
            "url": {"view_name": "snippet_detail"},
            "code": {"write_only": True},
            "language_choices": {"write_only": True},
            "style_choices": {"write_only": True},
            "category": {"write_only": True},
            "snippet_expiration": {"write_only": True},
        }
        read_only_fields = ["snippet_expired_date"]


class SnippetDetailSerializer(serializers.ModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name="highlight")
    author = serializers.StringRelatedField()
    password = serializers.CharField(write_only=True, allow_blank=True)

    class Meta:
        model = Snippet
        fields = [
            "url",
            "author",
            "category",
            "created",
            "title",
            "linenos",
            "code",
            "language_choices",
            "style_choices",
            "highlight",
            "view_once",
            "snippet_expiration",
            "snippet_expired_date",
            "password",
        ]
        extra_kwargs = {
            "url": {"view_name": "snippet_detail"},
        }
        read_only_fields = ["snippet_expired_date"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True,
        view_name="snippet_detail",
        read_only=True,
    )

    class Meta:
        model = get_user_model()
        fields = ["url", "username", "snippets"]
        extra_kwargs = {
            "url": {"view_name": "users_detail"},
        }
