import arrow
from django import template
from django.core.urlresolvers import reverse


register = template.Library()

@register.filter
def get_total_subject_posts(subject):

    total_posts = 0

    for thread in subject.threads.all():
        total_posts += thread.posts.count()

    return total_posts

@register.filter
def get_total_thread_posts(thread):

    total_posts = thread.posts.count()

    return total_posts

@register.simple_tag
def get_total_threads(subject):

    total_threads = subject.threads.count()

    return total_threads

@register.simple_tag
def get_total_thread_posts(thread):

    total_posts = thread.posts.count()

    return total_posts

@register.filter
def started_time(created_at):
   return arrow.get(created_at).humanize()


@register.filter
def last_posted_user_name(thread):
   posts = thread.posts.all().order_by('-created_at')
   print "number: %s" % posts
   # MH 20160925: check if there are any posts and return empty string if not
   # this avoids an index error
   if posts:
       # then get the top one
       post = thread.posts.all().order_by('-created_at')[0]
       first_name = post.user.first_name
       surname = post.user.last_name
       return "%s %s" % (first_name, surname)
   else:
       return ""


@register.filter
def get_num_subject_grids(subject):

    total_subjects = 0

    for sub in subject:

        total_subjects += 1

    #display max 4 in the grid
    if total_subjects > 4:
        total_subjects = 4

    return total_subjects