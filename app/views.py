from __future__ import annotations

import uuid

from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import get_user_model
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django_filters import rest_framework as filters
from rest_framework import generics, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.renderers import StaticHTMLRenderer
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView, Response

from . import models, serializers
from .filters import SnippetFilter
from .permissions import SnippetDetailPermission


@api_view(["GET"])
def entry_view(request):
    return Response(
        data={
            "users": request.build_absolute_uri(reverse("users")),
            "snippets": request.build_absolute_uri(reverse("snippets")),
        },
    )


class SnippetView(generics.ListCreateAPIView):
    permission_classes = [
        IsAuthenticatedOrReadOnly,
    ]
    serializer_class = serializers.SnippetListSerializer
    queryset = models.Snippet.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SnippetFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PasswordView(APIView):
    def get(self, request, pk):
        return Response("please enter your password.")

    def post(self, request, pk):
        password = request.data.get("password")
        print(password)
        snippet = models.Snippet.objects.get(pk=pk)
        print(snippet.password)
        if check_password(password, snippet.password):
            token = str(uuid.uuid4())
            cache.set(f"access_token_{pk}", token, timeout=3000)
            return Response({"password_token": token}, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid Password."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SnippetViewDetail(UpdateModelMixin, DestroyModelMixin, APIView):
    permission_classes = SnippetDetailPermission, IsAuthenticated

    def get(self, request, pk):
        snippet = get_object_or_404(models.Snippet, id=pk)
        checks = _checks(request, snippet, pk)
        if checks:
            return checks
        serializer = serializers.SnippetDetailSerializer(
            snippet,
            context={"request": request},
        )

        return Response(serializer.data)


class UserView(generics.ListCreateAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()


@api_view(["GET"])
@renderer_classes([StaticHTMLRenderer])
def highlighted_snippet_view(request, pk):
    snippet = get_object_or_404(models.Snippet, id=pk)
    checks = _checks(request, snippet, pk)
    if checks:
        return checks
    if snippet.view_once:
        if models.OneTimeCode.objects.filter(code=pk).exists():
            snippet.delete()
            return Response(
                status=HTTP_204_NO_CONTENT,
                data={"Snippet does not exist."},
            )
        else:
            models.OneTimeCode.objects.create(code=pk)
    data = snippet.highlighted
    return Response(data)


# helper function for checking password validation , view once and time expiration
def _checks(request, snippet, pk):

    if snippet.password:
        print(snippet.password)
        access_token = request.headers.get("X-Access-Token", "Not Given")
        valid_token = cache.get(f"access_token_{pk}")
        if access_token != valid_token:
            return redirect("password-required", pk)
    if snippet.snippet_expired_date:
        if timezone.now() >= snippet.snippet_expired_date:
            snippet.delete()
            return Response(status=HTTP_204_NO_CONTENT, data="Time has expired.")
