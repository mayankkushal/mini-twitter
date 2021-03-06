"""mini_twitter_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from mtweet import urls
from django.conf.urls.static import static
from django.conf import settings
from registration.backends.simple.views import RegistrationView
import notifications.urls



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('mtweet.urls')),
    url(r'^account/', include('registration.backends.simple.urls')),
    url(r'^friendship/', include('friendship.urls')),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
