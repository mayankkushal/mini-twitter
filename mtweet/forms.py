from django import forms
from mtweet.models import UserProfile, Post, Comment
from django.contrib.auth.models import User

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('firstname','lastname','gender','hometown','display_picture', 'mobile')


class PostForm(forms.ModelForm):
    likes = forms.IntegerField(widget=forms.HiddenInput, initial=0)
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        fields = ('content', )


class CommentForm(forms.ModelForm):
    comment = forms.CharField()

    class Meta:
        model = Comment
        fields = ('comment', )
