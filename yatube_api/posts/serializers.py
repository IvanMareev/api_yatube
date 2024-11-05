from rest_framework import serializers
from .models import Post, Group, Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'slug', 'description']


class PostSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(),
                                               allow_null=True, required=False)
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'pub_date', 'author', 'image', 'group']
        read_only_fields = ['author']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'text', 'created', 'post']
        read_only_fields = ['author', 'created', 'post']
