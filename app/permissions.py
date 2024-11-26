from __future__ import annotations

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class SnippetDetailPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        return False
