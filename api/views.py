from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Comment, Follow, User, Group
from .permissions import IsOwnerOrReadOnly
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group')
        if group is not None:
            queryset = queryset.filter(group__id=group)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset_post = Post.objects.all()
    queryset = Comment.objects.all()
    serializer_class_post = PostSerializer
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    # def list(self, request, pk, comment_pk=None):
    #     post = get_object_or_404(Post, pk=pk)
    #     if comment_pk:
    #         queryset = get_object_or_404(self.queryset, post=post, pk=comment_pk)
    #         return Response(self.serializer_class(queryset, many=False).data)
    #     queryset = get_list_or_404(Comment, post=post)
    #     return Response(self.serializer_class(queryset, many=True).data)

    def list(self, request, pk, comment_pk=None):
        post = get_object_or_404(Post, pk=pk)
        if comment_pk:
            queryset = get_object_or_404(self.queryset, post=post, pk=comment_pk)
            serializer = self.serializer_class(queryset, many=False)
            return Response(serializer.data)
        queryset = post.comments
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        post = get_object_or_404(self.queryset_post, pk=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, comment_pk):
        post = get_object_or_404(self.queryset_post, pk=pk)
        comment = get_object_or_404(self.queryset, post=post, pk=comment_pk)
        serializer = self.serializer_class(comment, data=request.data, partial=True)
        if self.request.user == comment.author:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk, comment_pk):
        post = get_object_or_404(self.queryset_post, pk=pk)
        comment = get_object_or_404(self.queryset, post=post, pk=comment_pk)
        if self.request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    queryset_user = User.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


"""
User - он подписывается
Following - на него подписываются
"""
