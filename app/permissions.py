from __future__ import annotations

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class SnippetDetailPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous:
            if request.user == obj.author:
                return True
        return False
