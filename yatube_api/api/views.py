from rest_framework.response import Response
from posts.models import Post, Group, Comment
from posts.serializers import PostSerializer
from posts.serializers import GroupSerializer, CommentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)

    @action(detail=True, methods=['get', 'post'], url_path='comments')
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.method == 'GET':
            comments = Comment.objects.filter(post=post)
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, post=post)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'PUT', 'PATCH', 'DELETE'],
            url_path='comments/(?P<comment_id>[^/.]+)')
    def comment_detail(self, request, pk=None, comment_id=None):
        post = get_object_or_404(Post, pk=pk)
        comment = get_object_or_404(Comment, pk=comment_id, post=post)

        if request.method == 'GET':
            serializer = CommentSerializer(comment)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            if comment.author != request.user:
                str = 'Редактирование чужого комментария запрещено!'
                raise PermissionDenied(str)
            serializer = CommentSerializer(comment, data=request.data,
                                           partial=(request.method == 'PATCH'))
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            if comment.author != request.user:
                str = 'Удаление чужого комментария запрещено!'
                raise PermissionDenied(str)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    http_method_names = ['get']
