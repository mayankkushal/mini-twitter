from django.conf.urls import url
from mtweet import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<username>[\w\-]+)/add_profile', views.add_profile, name="add_profile"),
    url(r'^home_page', views.home_page, name='home_page'),
    url(r'^(?P<username>[\w\-]+)/add_post', views.add_post, name='add_post'),
    url(r'^add_comment', views.add_comment, name='add_comment'),
    url(r'^show_post/(?P<pid>[\w\-]+)', views.show_post, name="show_post"),
    url(r'^like_post', views.like_post, name='like_post'),
    url(r'^show_user', views.show_user, name="show_user"),
    url(r'^profile/(?P<username>[\w\-]+)', views.profile, name='profile'),
    url(r'^add_follower', views.add_follower, name="add_follower")
]
