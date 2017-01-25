from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.OneToOneField(User)
    firstname = models.CharField(max_length=128)
    lastname = models.CharField(max_length=128)
    hometown = models.CharField(blank=True, max_length=128)
    display_picture = models.ImageField(blank=True)
    mobile = models.IntegerField(blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    follows = models.ManyToManyField('self', related_name='follower', symmetrical=False, blank=True)

    def __str__(self):
        return self.firstname


class Post(models.Model):
    user = models.ForeignKey(User)
    content = models.CharField(max_length=140, blank=False, help_text="Post")
    likes = models.IntegerField(default=0)
    post_time = models.DateTimeField(auto_now_add=True)
    comments = models.IntegerField(default=0)

    def __str__(self):
        return self.content

class Comment(models.Model):
    post = models.ForeignKey(Post)
    comment = models.CharField(max_length=128, blank=False, help_text='Comment')
    poster = models.CharField(blank=False, max_length=128)
    comment_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.poster

class Like(models.Model):
    user = models.ForeignKey(User)
    post = models.ForeignKey(Post)
    created = models.DateTimeField(auto_now_add=True)

