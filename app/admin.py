from django.contrib import admin
from .models import User,Snippet
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin import ModelAdmin

class SnippetAdmin(ModelAdmin):
    readonly_fields = ["highlighted"]

admin.site.register(Snippet,SnippetAdmin)
admin.site.register(User,UserAdmin)

