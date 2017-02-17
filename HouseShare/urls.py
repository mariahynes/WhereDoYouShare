"""HouseShare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from accounts import views as accounts_views
from home import views as home_views
from settings.base import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home_views.get_index, name='index'),
    url(r'^register/$', accounts_views.register, name='register'),
    url(r'^register_stripe/$', accounts_views.register_stripe, name='register_stripe'),
    url(r'^profile/$', accounts_views.profile, name='profile'),
    # url(r'^contact/$', home_views.contact, name='contact'),
    url(r'^pages/', include('django.contrib.flatpages.urls')),
    url(r'^login/$', accounts_views.login, name='login'),
    url(r'^logout/$', accounts_views.logout, name='logout'),
    url(r'^booking/', include('bookings.urls')),
    # url(r'^assets/', include('assets.urls')),
    url(r'^blog/', include('blog.urls')),
    url(r'^forum/', include('forum.urls')),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)