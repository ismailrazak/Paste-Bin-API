from rest_framework import serializers
from .models import Snippet,User
from django.contrib.auth.views import get_user_model


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    highlight = serializers.HyperlinkedIdentityField(view_name="highlight")
    author = serializers.StringRelatedField()
    password=serializers.CharField(write_only=True)
    class Meta:
        model = Snippet
        fields = ["url","author","created","title","linenos","code","language_choices","style_choices","highlight","view_once","snippet_expiration","snippet_expired_date","password"]
        extra_kwargs = {
            'url': {'view_name': 'snippet_detail'},
        }
        read_only_fields = ["snippet_expired_date"]

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True,view_name="snippet_detail",read_only=True)

    class Meta:
        model = get_user_model()
        fields = ["url",'username',"snippets"]
        extra_kwargs = {
            'url': {'view_name': 'users_detail'},
        }
