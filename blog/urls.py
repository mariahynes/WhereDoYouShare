from django.conf.urls import url
import views

urlpatterns = [
    url(r'^blog/(?P<asset_id>\d+)/$', views.post_list, name ="post_list"),
]