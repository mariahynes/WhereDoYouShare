from django.conf.urls import url
import views


urlpatterns = [
    url(r'^forum/(?P<asset_id>\d+)/$', views.forum, name ="forum"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/$', views.threads, name ="threads"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/$', views.thread, name ="thread"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/new/$', views.new_thread, name ="new_thread"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/new/$', views.new_post, name ="new_post"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/edit/$', views.edit_post, name ="edit_post"),
    url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/delete/$', views.delete_post, name ="delete_post"),

]