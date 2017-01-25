from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from mtweet.forms import PostForm, CommentForm, UserProfileForm
from mtweet.models import UserProfile, Post, Comment, Like
from django.contrib.auth.models import User
from friendship.models import Friend, Follow
from django.http import HttpResponse
import json
from django.core import serializers
from django.db.models.signals import post_save
from notifications.signals import notify


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, recipient=Post.user, verb='was saved')

def index(request):
	return render(request, 'mtweet/index.html')

@login_required
def home_page(request):
	user = request.user
	post_form = PostForm()
	post_list =[]
	profile = UserProfile.objects.get(user=user)
	all_following = Follow.objects.following(user)
	for following in all_following:
		post_list += Post.objects.filter(user=following).order_by('-post_time')
	def insertionSort(alist):
	   for index in range(1,len(alist)):
	    currentvalue = alist[index].post_time
	    currentuser = alist[index]
	    position = index
	    while position>0 and alist[position-1].post_time<currentvalue:
	        alist[position]=alist[position-1]
	        position = position-1
	    alist[position]=currentuser
	insertionSort(post_list)
	unread = user.notifications.unread()
	
	context_dict = {'post_form':post_form, 'post_list':post_list, 'unread':unread, 'profile':profile}
	return render(request, 'homepage/home_page.html', context_dict)

@login_required
def profile(request, username):
	user = request.user
	pro_user = User.objects.get(username=username)
	profile = UserProfile.objects.get(user=user)
	pro_profile = UserProfile.objects.get(user=pro_user)
	post_list_user = Post.objects.filter(user=user).order_by('-post_time')
	post_list_pro = Post.objects.filter(user=pro_user).order_by("-post_time")
	context_dict = {'user':user, 'profile':profile, 'pro_user':pro_user, 'pro_profile':pro_profile, 
					'post_list_user':post_list_user, 'post_list_pro':post_list_pro}
	return render(request, 'homepage/profile.html', context_dict)

@login_required
def show_user(request):
	user_list = User.objects.all().order_by('username')
	profile = UserProfile.objects.get(user=request.user)
	context_dict = {'user_list':user_list, 'profile':profile}
	return render(request, 'homepage/show_user.html', context_dict)

def add_profile(request, username):
	user = request.user
	if request.method == 'POST':
		profileform = UserProfileForm(request.POST)
		if profileform.is_valid():
			profile = profileform.save(commit=False)
			profile.user = user
			profile.save()
		return redirect(home_page)
	else:
		profileform = UserProfileForm()
	return render(request, 'mtweet/add_profile.html', {'profileform':profileform})

@login_required
def add_post(request):
	user = request.user
	if request.method == 'POST':
		content = request.POST['content']
		Post.objects.create(
				user=user,
				content=content,
			)

		return HttpResponse('')
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
			post.comments += 1
			post.save()
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
			new_like, created = Like.objects.get_or_create(user=request.user, post_id=pid)
			if not created:
				new_like.delete()
				liked = False
			else:
				liked = True
			count = Like.objects.filter(post=post).count()
			data = {'count':count, 'liked':liked}
			return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def add_follower(request):
	if request.method == "GET":
		username = request.GET['username']
		follow_user = User.objects.get(username=username)
		Follow.objects.add_follower(request.user, follow_user)
		return HttpResponse('')


def like_count(request):
	if request.method == "GET":
		pid = request.GET['pid']
		post = get_object_or_404(Post, id=pid)
		liked = Like.objects.filter(user=request.user, post=post)
		if liked:
			liked_this = True
		else:
			liked_this = False
		count = Like.objects.filter(post=post).count()
		data = {}
		data['count'] = count
		data['liked_this'] = liked_this
		return HttpResponse(json.dumps(data), content_type='application/json')

def in_search(request):
	if request.method == 'GET':
		usr_lst = []
		search = request.GET['search']
		if search == '':
			return HttpResponse('')
		serial = serializers.serialize('json', User.objects.filter(username__istartswith=search), fields=('username'))
		return HttpResponse(serial, content_type='application/json')
		
