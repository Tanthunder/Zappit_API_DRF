from django.shortcuts import render
from rest_framework import generics , permissions , mixins, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Post , Vote
from .serializers import PostSerializer , VoteSerializer


class PostList(generics.ListCreateAPIView):
    """class based view for listing data for post model. """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """"""
        serializer.save(poster = self.request.user)


class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    """class based view for listing data for post model. """
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        """Only crator of post can delete it."""
        post = Post.objects.filter(pk=kwargs['pk'], poster = self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else :
            raise ValidationError('This post is not yours.')

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    """class based view for lcreating vote. """
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """"""
        user = self.request.user
        post = Post.objects.get(pk = self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        """"""
        if self.get_queryset().exists():
            raise ValidationError("you have already voted")
        serializer.save(voter = self.request.user, post = Post.objects.get(pk = self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        """"""
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else :
            raise ValidationError('You never voted for this post')