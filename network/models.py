from django.contrib.auth.models import AbstractUser
from django.db import models

from annoying.fields import AutoOneToOneField


class User(AbstractUser):
    pass


class Profile(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="profile")
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")

    def __str__(self):
        return f"{self.user}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=260)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        timestamp = self.timestamp.strftime("%b %d %Y, %-I:%M %p")
        return f"{self.user} on {timestamp}"
