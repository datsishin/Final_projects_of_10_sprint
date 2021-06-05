from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Post, Comment, Follow, User, Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username', default=serializers.CurrentUserDefault())
    following = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following']
            )
        ]
        fields = '__all__'
        model = Follow


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    # group = serializers.ReadOnlyField(source='group.id')

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.ReadOnlyField(source='post.id')

    class Meta:
        fields = '__all__'
        model = Comment


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group
