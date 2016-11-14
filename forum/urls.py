from django.conf.urls import url
import views


urlpatterns = [
    url(r'^forum/(?P<asset_id>\d+)/$', views.forum, name ="forum"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/$', views.threads, name ="threads"),
]