from __future__ import annotations

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from .models import Snippet, User

# Register your models here.


class SnippetAdmin(ModelAdmin):
    readonly_fields = ["highlighted"]


admin.site.register(Snippet, SnippetAdmin)
admin.site.register(User, UserAdmin)
