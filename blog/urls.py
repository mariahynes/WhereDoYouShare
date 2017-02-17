from django.conf.urls import url
import views

urlpatterns = [
    url(r'^blog/(?P<asset_id>\d+)/$', views.post_list, name ="post_list"),
    url(r'^blog/(?P<asset_id>\d+)/(?P<id>\d+)/$', views.post_detail, name ="post_detail"),
    url(r'^blog/(?P<asset_id>\d+)/new/$', views.new_blog_post, name ="new_blog_post"),
    url(r'^blog/(?P<asset_id>\d+)/(?P<id>\d+)/edit/$', views.edit_blog_post, name ="edit_blog_post"),
    url(r'^blog/(?P<asset_id>\d+)/(?P<id>\d+)/delete/$', views.delete_blog_post, name ="delete_blog_post"),
]