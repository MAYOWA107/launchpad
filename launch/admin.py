from django.contrib import admin

from .models import Ideas, Category, Vote, Comment


admin.site.register(Ideas)
admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Comment)
