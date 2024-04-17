from django.contrib import admin
from .models import (
    Post, FollowUser, LikePost,
    Comment,
)

admin.site.register(Post)
admin.site.register(FollowUser)
admin.site.register(LikePost)
admin.site.register(Comment)
