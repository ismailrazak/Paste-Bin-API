from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("", views.entry_view, name="entry_view"),
    path("snippets/", views.SnippetView.as_view(), name="snippets"),
    path("snippets/<str:pk>", views.SnippetViewDetail.as_view(), name="snippet_detail"),
    path(
        "snippets/<str:pk>/highlighted",
        views.highlighted_snippet_view,
        name="highlight",
    ),
    path("users", views.UserView.as_view(), name="users"),
    path("users/<str:pk>", views.UserDetailView.as_view(), name="users_detail"),
    path(
        "password-required/<str:pk>",
        views.PasswordView.as_view(),
        name="password-required",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)
