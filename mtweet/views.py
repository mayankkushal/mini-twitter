from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mtweet.forms import PostForm, CommentForm, UserProfileForm
from mtweet.models import UserProfile, Post, Comment
from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from django.http import HttpResponse
import json

def index(request):
	return render(request, 'mtweet/index.html')

@login_required
def home_page(request):
	user = request.user
	post_form = PostForm()
	post_list =[]
	all_following = Follow.objects.following(user)
	for following in all_following:
		post_list += Post.objects.filter(user=following).order_by('-post_time')
	context_dict = {'user':user, 'post_form':post_form, 'post_list':post_list}
	return render(request, 'homepage/home_page.html', context_dict)

@login_required
def profile(request, username):
	user = request.user
	pro_user = User.objects.get(username=username)
	profile = UserProfile.objects.get(user=user)
	pro_profile = UserProfile.objects.get(user=pro_user)
	context_dict = {'user':user, 'profile':profile, 'pro_user':pro_user, 'pro_profile':pro_profile}
	return render(request, 'homepage/profile.html', context_dict)

@login_required
def show_user(request):
	user_list = User.objects.all().order_by('username')
	context_dict = {'user_list':user_list}
	return render(request, 'homepage/show_user.html', context_dict)

def add_profile(request, username):
	user = request.user
	if request.method == 'POST':
		profileform = UserProfileForm(request.POST)
		if profileform.is_valid():
			profile = profileform.save(commit=False)
			profile.user = user
			profile.save()
		return home_page(request)
	else:
		profileform = UserProfileForm()
	return render(request, 'mtweet/add_profile.html', {'profileform':profileform})

@login_required
def add_post(request, username):
	user = request.user
	if request.method == 'POST':
		postform = PostForm(request.POST)
		if postform.is_valid():
			post = postform.save(commit=False)
			post.user = user
			post.save()
		return home_page(request)
	else:
		return home_page(request)

@login_required
def show_post(request, pid):
	comment_form = CommentForm()
	comment_list = None
	try:
		post = Post.objects.get(id=pid)
	except Post.DoesNotExist:
		post = None
	if post:
		comment_list = Comment.objects.filter(post=post).order_by('-comment_time')
		context_dict = {'post':post, 'comment_form':comment_form, 'comment_list':comment_list}
		return render(request, 'homepage/show_post.html', context_dict)
	else:
		return HttpResponse("No such post")

@login_required
def add_comment(request):
	if request.method == 'POST':
		comment = request.POST['comment']
		pid = request.POST['pid']
		post = Post.objects.get(id=pid)
		if post:
			Comment.objects.create(
					post=post,
					comment=comment,
					poster=request.user.username
				)
			data = {}
			data['comment'] = comment
			data['user'] = request.user.username
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			return HttpResponse("No such post")

@login_required
def like_post(request):
	if request.method == "GET":
		pid = request.GET['pid']
		post = Post.objects.get(id=pid)
		if post:
			likes = post.likes + 1
			post.likes = likes
			post.save()
			return HttpResponse(likes)

@login_required
def add_follower(request):
	if request.method == "GET":
		username = request.GET['username']
		follow_user = User.objects.get(username=username)
		Follow.objects.add_follower(request.user, follow_user)
		return HttpResponse('')

