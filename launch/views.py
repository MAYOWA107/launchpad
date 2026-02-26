from django.shortcuts import render
from .models import Ideas, Category, Comment, Vote
from .serializers import (
    IdeasSerializer,
    VoteSerializer,
    CategorySerializer,
    CommentSerializer,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend


class IdeasView(ListAPIView):
    queryset = Ideas.objects.all().order_by("-created_at")
    serializer_class = IdeasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "category"]


class MyIdeaView(ListCreateAPIView):
    serializer_class = IdeasSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["title", "category"]

    def get_queryset(self):
        return Ideas.objects.filter(author=self.request.user).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IdeaDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Ideas.objects.all()
    serializer_class = IdeasSerializer


class CategoryView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["name", "excerpt"]

    def get_queryset(self):
        return Category.objects.annotate(total_ideas=Count("ideas"))


class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class VoteView(CreateAPIView):
    serializer_class = VoteSerializer
    queryset = Vote.objects.all()

    def perform_create(self, serializer):
        idea = get_object_or_404(Ideas, id=self.kwargs["idea_id"])

        if Vote.objects.filter(user=self.request.user, idea=idea).exists():
            raise ValidationError("You've already voted for this idea.")

        serializer.save(user=self.request.user, idea=idea)


class VoteDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


class CommentView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class IdeaComment(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        idea_id = self.kwargs["idea_id"]
        return Comment.objects.filter(idea_id=idea_id)

    def perform_create(self, serializer):
        idea_id = self.kwargs["idea_id"]
        idea = get_object_or_404(Ideas, id=idea_id)
        serializer.save(user=self.request.user, idea=idea)


class TrendingIdeasView(ListAPIView):
    serializer_class = IdeasSerializer

    def get_queryset(self):
        return Ideas.objects.annotate(total_votes=Count("votes")).order_by(
            "-total_votes"
        )
