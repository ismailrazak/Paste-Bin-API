from rest_framework.permissions import BasePermission
from rest_framework import permissions


class SnippetDetailPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        return False


class HomeViewPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user == obj.author:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
