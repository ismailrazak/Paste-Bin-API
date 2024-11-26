from __future__ import annotations

import uuid
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100)
    code = models.TextField()
    language_choices = models.CharField(
        choices=LANGUAGE_CHOICES,
        default="Python",
        max_length=100,
    )
    style_choices = models.CharField(
        choices=STYLE_CHOICES,
        default="friendly",
        max_length=100,
    )
    linenos = models.BooleanField(default=False)
    highlighted = models.TextField(null=True, blank=True)
    view_once = models.BooleanField(default=False)
    password = models.CharField(max_length=300, blank=True)
    snippet_expired_date = models.DateTimeField(null=True, blank=True)

    class CategoryChoices(models.TextChoices):
        gaming = "GA", "gaming"
        software = "SO", "software"
        source_code = "SC", "source code"
        writing = "WR", "writing"
        AI = "AI", "Artifical Intelligence"
        misc = "MI", "Miscellaneous"
        help = "HE", "Help"

    class SnippetExpirationChoices(models.TextChoices):
        never = "NO", "never"
        ten_min = "10", "10 minutes"
        one_hour = "1H", "one hour"
        one_day = "1D", "one day"
        one_week = "1W", "one week"
        one_month = "1M", "one month"

    category = models.CharField(
        max_length=2,
        choices=CategoryChoices,
        default=CategoryChoices.software,
    )
    snippet_expiration = models.CharField(
        max_length=2,
        choices=SnippetExpirationChoices,
        default=SnippetExpirationChoices.never,
    )

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        _internal_time = {
            "NO": None,
            "10": timedelta(minutes=10),
            "1H": timedelta(hours=1),
            "1D": timedelta(days=1),
            "1W": timedelta(weeks=1),
            "1M": timedelta(days=30),
        }
        if _internal_time[self.snippet_expiration]:
            self.snippet_expired_date = (
                timezone.now() + _internal_time[self.snippet_expiration]
            )
        lexer = get_lexer_by_name(self.language_choices)
        linenos = "table" if self.linenos else False
        options = {"title": self.title} if self.title else {}
        formatter = HtmlFormatter(
            style=self.style_choices,
            linenos=linenos,
            full=True,
            **options,
        )
        self.highlighted = highlight(self.code, lexer, formatter)
        super().save(*args, **kwargs)


class OneTimeCode(models.Model):
    code = models.CharField(max_length=200)

    def __str__(self):
        return self.code
