from django.test import TestCase
from blog.models import Post
from .views import post_list, post_detail, new_blog_post, edit_blog_post
from assets.models import Asset
from django.core.urlresolvers import resolve


class PostTests(TestCase):

    def test_str(self):
        test_title = Post(title="Sample Title")
        self.assertEquals(str(test_title),"Sample Title")


class BlogPageTest(TestCase):

    fixtures = ['assets', 'user', 'post']
    # url(r'^blog/(?P<asset_id>\d+)/$', views.post_list, name ="post_list"),
    def test_blog_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/blog/blog/%s/' % asset_id
        blog_page = resolve(the_url)
        self.assertEqual(blog_page.func, post_list)

    # url(r'^blog/(?P<asset_id>\d+)/(?P<id>\d+)/$', views.post_detail, name ="post_detail"),
    def test_blog_post_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        post = Post.objects.all().filter(asset_ID_id=asset_id)[0]
        post_id = post.id
        the_url = '/blog/blog/%s/%s/' % (asset_id, post_id)
        blog_page = resolve(the_url)
        self.assertEqual(blog_page.func, post_detail)

    # url(r'^blog/(?P<asset_id>\d+)/new/$', views.new_blog_post, name ="new_blog_post"),
    def test_blog_new_post_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/blog/blog/%s/new/' % asset_id
        blog_page = resolve(the_url)
        self.assertEqual(blog_page.func, new_blog_post)

    # url(r'^blog/(?P<asset_id>\d+)/(?P<id>\d+)/edit/$', views.edit_blog_post, name ="edit_blog_post"),
    def test_blog_edit_post_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        post = Post.objects.all().filter(asset_ID_id=asset_id)[0]
        post_id = post.id
        the_url = '/blog/blog/%s/%s/edit/' % (asset_id, post_id)
        blog_page = resolve(the_url)
        self.assertEqual(blog_page.func, edit_blog_post)