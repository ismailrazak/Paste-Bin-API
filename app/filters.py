from django_filters import rest_framework as filters
from .models import Snippet


class SnippetFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    tags = filters.CharFilter(field_name="tags__name", lookup_expr="in")

    class Meta:
        model = Snippet
        fields = ["author"]
