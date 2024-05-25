from django.db import models
from django.contrib.auth.models import User
from config.base_models import BaseModel


class Post(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/posts/')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    is_published = models.BooleanField(default=True)

    def number_of_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.author.username


class Comment(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    message = models.CharField(max_length=120)

    def __str__(self):
        return self.author.username


class LikePost(BaseModel):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username


class FollowUser(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.follower.username
