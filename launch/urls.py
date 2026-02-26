from django.urls import path
from . import views


urlpatterns = [
    path("ideas", views.IdeasView.as_view(), name="ideas"),
    path("idea/<int:pk>", views.IdeaDetailView.as_view(), name="idea"),
    path("categories", views.CategoryView.as_view(), name="categories"),
    path("category/<int:pk>", views.CategoryDetailView.as_view(), name="category"),
    path("ideas/<int:idea_id>/vote/", views.VoteView.as_view(), name="votes"),
    path("vote/<int:pk>", views.VoteDetailView.as_view(), name="vote"),
    path("comments", views.CommentView.as_view(), name="comments"),
    path("comment/<int:pk>", views.CommentDetailView.as_view(), name="comment"),
    path("my-ideas", views.MyIdeaView.as_view(), name="my_ideas"),
    path(
        "ideas/<int:idea_id>/comments", views.IdeaComment.as_view(), name="idea-comment"
    ),
    path("ideas/trending", views.TrendingIdeasView.as_view(), name="ideas-trending"),
]
