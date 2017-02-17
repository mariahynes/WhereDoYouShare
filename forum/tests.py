from django.test import TestCase
from django.shortcuts import render_to_response
from .models import Subject, Thread, Post
from assets.models import Asset
from django.core.urlresolvers import resolve
from .views import forum, threads, thread,new_thread, new_post, edit_post, delete_post


class ForumPageTest(TestCase):

    fixtures = ['assets', 'user', 'subjects']

    # url(r'^forum/(?P<asset_id>\d+)/$', views.forum, name="forum"),
    def test_forum_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        the_url = '/forum/forum/%s/' % asset_id
        forum_page = resolve(the_url)
        self.assertEqual(forum_page.func, forum)


    # url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/$', views.threads, name="threads"),
    def test_threads_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        subject = Subject.objects.all().filter(asset_id_id=asset_id)[0]
        subject_id = subject.id
        the_url = '/forum/forum/%s/%s/' % (asset_id, subject_id)
        thread_page = resolve(the_url)
        self.assertEqual(thread_page.func, threads)

    # url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/new/$', views.new_thread, name="new_thread"),
    def test_new_threads_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        subject = Subject.objects.all().filter(asset_id_id=asset_id)[0]
        subject_id = subject.id
        the_url = '/forum/forum/%s/%s/new/' % (asset_id, subject_id)
        thread_page = resolve(the_url)
        self.assertEqual(thread_page.func, new_thread)

    # url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/$', views.thread, name="thread"),
    def test_thread_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        subject = Subject.objects.all().filter(asset_id_id=asset_id)[0]
        subject_id = subject.id
        threads = Thread.objects.all().filter(subject_id=subject_id)[0]
        thread_id = threads.id
        the_url = '/forum/forum/%s/%s/%s/' % (asset_id, subject_id, thread_id)
        thread_page = resolve(the_url)
        self.assertEqual(thread_page.func, thread)


    # url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/new/$', views.new_post, name="new_post"),
    def test_new_thread_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        subject = Subject.objects.all().filter(asset_id_id=asset_id)[0]
        subject_id = subject.id
        threads = Thread.objects.all().filter(subject_id=subject_id)[0]
        thread_id = threads.id
        the_url = '/forum/forum/%s/%s/%s/new/' % (asset_id, subject_id, thread_id)
        thread_page = resolve(the_url)
        self.assertEqual(thread_page.func, new_post)

    # url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/edit/$', views.edit_post,
    #     name="edit_post"),
    def test_edit_post_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        subject = Subject.objects.all().filter(asset_id_id=asset_id)[0]
        subject_id = subject.id
        threads = Thread.objects.all().filter(subject_id=subject_id)[0]
        thread_id = threads.id
        posts = Post.objects.all().filter(thread_id=thread_id)[0]
        post_id = posts.id
        the_url = '/forum/forum/%s/%s/%s/%s/edit/' % (asset_id, subject_id, thread_id, post_id)
        post_page = resolve(the_url)
        self.assertEqual(post_page.func, edit_post)

    # url(r'^forum/(?P<asset_id>\d+)/(?P<subject_id>\d+)/(?P<thread_id>\d+)/(?P<post_id>\d+)/delete/$', views.delete_post,
    #     name="delete_post"),
    def test_delete_post_page_resolved(self):
        asset = Asset.objects.all()[0]
        asset_id = asset.id
        subject = Subject.objects.all().filter(asset_id_id=asset_id)[0]
        subject_id = subject.id
        threads = Thread.objects.all().filter(subject_id=subject_id)[0]
        thread_id = threads.id
        posts = Post.objects.all().filter(thread_id=thread_id)[0]
        post_id = posts.id
        the_url = '/forum/forum/%s/%s/%s/%s/delete/' % (asset_id, subject_id, thread_id, post_id)
        post_page = resolve(the_url)
        self.assertEqual(post_page.func, delete_post)
