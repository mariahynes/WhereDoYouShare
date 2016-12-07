from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Thread, Post
from home.myAuth import check_user_linked_to_asset, check_thread_exists,check_subject_exists,check_user_linked_to_forum_post
from assets.models import Asset
from django.contrib.auth.decorators import login_required
from .forms import ThreadForm, PostForm
from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf

@login_required(login_url='/login/')
def forum(request, asset_id):

    errors = []

    # check that the asset ID exists
    # if not a 404 will be thrown
    the_asset = get_object_or_404(Asset, pk=asset_id)

    # ok, so asset exists
    # now check that this user is allowed to view the forum subjects for this asset
    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id):
        # user is linked so fill up the subjects object
        subjects = Subject.objects.all().filter(asset_id=asset_id)

    else:
        # prepare the error message
        errors.append("You are not authorised to view this Forum")
        # set these to empty
        the_asset = []
        subjects = []

    return render(request, 'forum.html',{'subjects': subjects, 'asset': the_asset, 'errors': errors})

@login_required(login_url='/login/')
def threads(request, asset_id, subject_id):

    # this view shows all threads for a given subject
    errors = []
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id)==False:
        errors.append("You are not authorised to view this Forum")
        subject = []
        the_asset = []

    if check_subject_exists(asset_id, subject_id) == False:
        errors.append("Sorry this Subject does not exist in this Forum")
        subject = []
        the_asset = []

    return render(request, "threads.html",{'subject': subject, 'asset': the_asset, 'errors': errors})

@login_required(login_url='/login/')
def thread(request, asset_id, subject_id, thread_id):

    # this view shows the one thread only
    errors = []
    content_error = ""
    thread = get_object_or_404(Thread, pk=thread_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id) == False:
        errors.append("You are not authorised to view to this Forum")
        thread = []
        subject = []
        the_asset = []

    if check_subject_exists(asset_id, subject_id) == False:
        errors.append("Sorry this Subject does not exist in this Forum")
        thread = []
        subject = []
        the_asset = []

    if check_thread_exists(subject_id ,thread_id) == False:
        errors.append("Thread does not exist")
        thread = []
        subject = []
        the_asset = []
    else:
        # it can be viewed so update the counter
        thread.num_views += 1
        thread.save()

    args = {
        'thread': thread,
        'errors': errors,
        'subject': subject,
        'asset': the_asset,
    }
    args.update(csrf(request))

    return render(request, 'thread.html', args)

@login_required(login_url='/login/')
def new_thread(request, asset_id, subject_id):

    errors = []
    content_error = ""
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id)==False:
        errors.append("You are not authorised to add to this Forum")
        subject = []
        the_asset = []

    elif check_subject_exists(asset_id, subject_id) == False:
            errors.append("Sorry this Subject does not exist in this Forum")
            subject = []
            the_asset = []

    else:

        if request.method == "POST":
            thread_form = ThreadForm(request.POST)
            post_form = PostForm(request.POST)

            if thread_form.is_valid() and post_form.is_valid():

                # before saving check the content of the comment field
                if len(post_form.cleaned_data['comment']) == 0:
                    thread_form = ThreadForm(request.POST)
                    post_form = PostForm(request.POST)
                    content_error = "Please don't save your new thread without posting a starting comment!"

                else:
                    thread = thread_form.save(False)
                    thread.subject = subject
                    thread.user = request.user
                    thread.save()

                    post = post_form.save(False)
                    post.user = request.user
                    post.thread = thread
                    post.save()

                    messages.success(request, "Thanks for your new Thread")

                    return redirect(reverse('thread', kwargs={"asset_id":asset_id, "subject_id":subject_id, "thread_id":thread.pk}))

        else:
            thread_form = ThreadForm()
            post_form = PostForm(request.POST)

    args = {
        'thread_form': thread_form,
        'post_form': post_form,
        'subject': subject,
        'asset': the_asset,
        'errors': errors,
        'content_error': content_error
    }
    args.update(csrf(request))

    return render(request,'thread_form.html', args)

@login_required(login_url='/login/')
def new_post(request, asset_id, subject_id, thread_id):

    # this view allows the user to add a post to a thread
    errors = []
    content_error = ""
    thread = get_object_or_404(Thread, pk=thread_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)
    # set this here so that it is assigned
    form = PostForm()

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id) == False:
        errors.append("You are not authorised to view to this Forum")
        thread = []
        subject = []
        the_asset = []

    elif check_subject_exists(asset_id, subject_id) == False:
        errors.append("Sorry this Subject does not exist in this Forum")
        thread = []
        subject = []
        the_asset = []

    elif check_thread_exists(subject_id, thread_id) == False:
        errors.append("Thread does not exist")
        thread = []
        subject = []
        the_asset = []

    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():

                # before saving check the content of the comment field
                if len(form.cleaned_data['comment']) == 0:
                    form = PostForm(request.POST)
                    content_error = "Please don't save a blank post!"
                else:
                    post = form.save(False)
                    post.thread = thread
                    post.user = request.user
                    post.save()

                    messages.success(request, "Your post has been added to %s" % thread.name)

                    return redirect(reverse('thread', kwargs={"asset_id":asset_id, "subject_id":subject_id, "thread_id":thread.pk}))

            else:
                form = PostForm()

    args = {
            'thread': thread,
            'errors': errors,
            'subject': subject,
            'asset': the_asset,
            'form': form,
            'form_action': reverse('new_post', kwargs={"asset_id":asset_id, "subject_id":subject_id, "thread_id":thread.id}),
            'button_text': "Update Post",
            'content_error':content_error,
    }
    args.update(csrf(request))

    return render(request, 'post_form.html', args)

@login_required(login_url='/login/')
def edit_post(request, asset_id, subject_id, thread_id, post_id):
    # this sends user to the post_form.html mentioned in the new_post view (for editing)
    # and to thread.html for viewing after editing
    errors = []
    content_error = ""
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=thread_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id) == False:
        errors.append("You are not authorised to view to this Forum")
        post = []
        thread = []
        subject = []
        the_asset = []

    elif check_subject_exists(asset_id, subject_id) == False:
        errors.append("Sorry this Subject does not exist in this Forum")
        post = []
        thread = []
        subject = []
        the_asset = []

    elif check_thread_exists(subject_id, thread_id) == False:
        errors.append("Thread does not exist")
        post = []
        thread = []
        subject = []
        the_asset = []

    elif check_user_linked_to_forum_post(my_id, post_id) == False:
        errors.append("You are not authorised to edit this Post")
        post = []
        thread = []
        subject = []
        the_asset = []

    else:
        if request.method == "POST":
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                # before saving check the content of the comment field
                if len(form.cleaned_data['comment']) == 0:
                    post = get_object_or_404(Post, pk=post_id)
                    form = PostForm(instance=post)
                    content_error = "Please don't save a blank post!"
                else:
                    form.save()
                    messages.success(request,"This Post has been updated")

                    return redirect(reverse('thread', kwargs={"asset_id":asset_id, "subject_id":subject_id, "thread_id":thread.pk}))

        else:
            form = PostForm(instance=post)

    args = {
        'thread': thread,
        'errors': errors,
        'subject': subject,
        'asset': the_asset,
        'form': form,
        'form_action': reverse('edit_post', kwargs={'asset_id':asset_id, "subject_id":subject_id, "thread_id":thread_id, "post_id":post_id}),
        'button_text': "Update Post",
        'content_error':content_error,
    }
    args.update(csrf(request))

    return render(request, 'post_form.html', args)

@login_required(login_url='/login/')
def delete_post(request, asset_id, subject_id, thread_id, post_id):

    errors = []
    post = get_object_or_404(Post, pk=post_id)
    thread = get_object_or_404(Thread, pk=thread_id)
    subject = get_object_or_404(Subject, pk=subject_id)
    the_asset = get_object_or_404(Asset, pk=asset_id)

    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id) == False:
        errors.append("You are not authorised to view to this Forum")
        post = []
        thread = []
        subject = []
        the_asset = []

    elif check_subject_exists(asset_id, subject_id) == False:
        errors.append("Sorry this Subject does not exist in this Forum")
        post = []
        thread = []
        subject = []
        the_asset = []

    elif check_thread_exists(subject_id, thread_id) == False:
        errors.append("Thread does not exist")
        post = []
        thread = []
        subject = []
        the_asset = []

    elif check_user_linked_to_forum_post(my_id, post_id) == False:
        errors.append("You are not authorised to edit this Post")
        post = []
        thread = []
        subject = []
        the_asset = []

    else:
        post.delete()

        messages.success(request, "This Post has been deleted")

        return redirect(reverse('thread', kwargs={"asset_id":asset_id, "subject_id":subject_id, "thread_id":thread_id}))