from django.db import models
from accounts.models import CustomUser
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=100)
    excerpt = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Ideas(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="ideas"
    )
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="ideas"
    )
    short_description = models.TextField(max_length=50)
    long_description = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "ideas"

    def __str__(self):
        return self.title


class Vote(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    idea = models.ForeignKey(Ideas, on_delete=models.PROTECT, related_name="votes")
    value = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user} voted for {self.idea}"

    class Meta:
        unique_together = ["user", "idea"]


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    idea = models.ForeignKey(Ideas, on_delete=models.PROTECT, related_name="comments")
    comment = models.TextField()

    def __str__(self):
        return self.comment[:50] + "...."
