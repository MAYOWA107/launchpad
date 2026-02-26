from rest_framework import serializers
from .models import Ideas, Category, Vote, Comment


class IdeasSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Ideas
        fields = [
            "title",
            "category",
            "author",
            "short_description",
            "long_description",
            "total_votes",
        ]
        # read_only = ["author"]


class CategorySerializer(serializers.ModelSerializer):
    total_ideas = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = ["id", "name", "excerpt", "total_ideas"]


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    idea = serializers.PrimaryKeyRelatedField(queryset=Ideas.objects.all())

    class Meta:
        model = Vote
        fields = ["user", "idea"]
        read_only = ["user"]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ["user", "idea", "comment"]
        read_only = ["user"]
