from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Post
from home.myAuth import check_user_linked_to_asset,blog_post_exists,check_user_linked_to_blog_post
from assets.models import Asset
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
import json
from django.template.context_processors import csrf
from django.contrib import messages
from django.core.urlresolvers import reverse

@login_required(login_url='/login/')
def post_list(request, asset_id):

    # this view will return the posts for the given asset_id
    # posts will be ordered by most recent first and
    # only posts with pub date from current date or before

    errors = []

    # check that the asset ID exists
    # if not a 404 will be thrown
    the_asset = get_object_or_404(Asset, pk=asset_id)

    # ok, so asset exists
    # now check that this user is allowed to view posts for this asset
    my_id = request.user

    #if check_user_linked_to_asset(my_id, asset_id):
    if check_user_linked_to_asset(my_id, asset_id):
        # user is linked so fill up the posts object
        posts = Post.objects.filter(asset_ID=asset_id, published_date__lte=timezone.now()).order_by('-published_date')

    else:
        # prepare the error message
        errors.append("You are not authorised to view this Blog")
        # set these to empty
        the_asset = []
        posts = []

    # save this current asset_id in sessions
    # over-writing what's save already
    request.session['current_asset_id'] = asset_id

    num_linked_assets = request.session['linked_assets']
    j = json.loads(num_linked_assets)

    return render(request, "blogposts.html", {'posts': posts, 'asset':the_asset, 'errors':errors, 'num_linked_assets':j})

@login_required(login_url='/login/')
def post_detail(request, asset_id, id):

    errors = []
    show_edit = False # defaults to False

    # this view is of one post
    # need to check user is authorised to view it
    # and if they are the AUTHOR, they will see an edit button

    #  first check does the post exist?
    if blog_post_exists(asset_id,id) == False:

        errors.append("This page does not exist")
        post = []
        the_asset = []

    else:
        # it does exist
        post = Post.objects.get(id=id, asset_ID_id=asset_id)
        the_asset = get_object_or_404(Asset, pk=asset_id)

        # but now check that this user is allowed to view posts for this asset
        my_id = request.user

        if check_user_linked_to_asset(my_id, asset_id) == False:

            # prepare the error message
            errors.append("You are not authorised to view this Post")
            # set these to empty
            the_asset = []
            post = []

        else:
            # it can be viewed so update the counter
            post.num_views += 1
            post.save()

            #is this person the author?
            if check_user_linked_to_blog_post(my_id,asset_id,id):
                show_edit = True


    return render(request, "postdetail.html", {'post':post, 'asset': the_asset, 'errors': errors, 'asset_id': asset_id,'post_id':id, 'show_edit':show_edit})

@login_required(login_url='/login/')
def new_blog_post(request, asset_id):
    errors = []
    the_asset = get_object_or_404(Asset, pk=asset_id)
    form = []
    content_error = ""

    # asset exists, now check user
    my_id = request.user
    if check_user_linked_to_asset(my_id, asset_id) == False:
        # user is linked so fill up the posts object
        errors.append("You are not authorised to post on this Blog")
        the_asset = []

    else:
        # check POST or GET
        if request.method == "POST":

            form = BlogPostForm(request.POST, request.FILES)
            if form.is_valid():
                # before saving check the content of the content field
                if len(form.cleaned_data['content']) == 0:
                    # check if content is blank. HTML Field has to be set to required == False
                    # so that the form can submit (to do with the browser trying to focus on the element and not seeing it
                    # so it's possible that it's blank
                    form = BlogPostForm(request.POST)
                    content_error = "Please don't save your new post without some content!"

                else:
                    post = form.save(commit=False)
                    post.author = request.user
                    post.published_date = timezone.now()
                    post.asset_ID_id = asset_id
                    post.save()
                    return redirect(post_detail, asset_id, post.pk)

        else:
            form = BlogPostForm()

    args = {
        'errors': errors,
        'asset': the_asset,
        'form': form,
        'content_error': content_error

    }
    args.update(csrf(request))

    return render(request, 'blogpostform.html', args)

@login_required(login_url='/login/')
def edit_blog_post(request, asset_id, id):

    errors = []
    content_error = ""
    form = []
    the_asset = []

    #  first check does the post exist?
    if blog_post_exists(asset_id, id) == False:

        errors.append("This page does not exist")

    else:
        # it does exist
        post = Post.objects.get(id=id, asset_ID_id=asset_id)
        the_asset = get_object_or_404(Asset, pk=asset_id)

        # but now check that this user is allowed to view posts for this asset
        my_id = request.user

        if check_user_linked_to_asset(my_id, asset_id) == False:
            # prepare the error message
            errors.append("You are not authorised to edit this Post")
            # set these to empty
            the_asset = []


        # and finally check if the user is the one who CREATED this post
        # only they should be allowed to edit (or the staff)

        if check_user_linked_to_blog_post(my_id, asset_id, id) == False and request.user.is_staff == False:
            errors.append("You are not authorised to edit this Post")
            # set these to empty
            the_asset = []


        if request.method == "POST":
            form = BlogPostForm(request.POST, request.FILES, instance=post)

            if form.is_valid():
                if len(form.cleaned_data['content']) == 0:
                    # check if content is blank. HTML Field has to be set to required == False
                    # so that the form can submit (to do with the browser trying to focus on the element and not seeing it
                    # so it's possible that it's blank
                    post = Post.objects.get(id=id, asset_ID_id=asset_id)
                    form = BlogPostForm(instance=post)
                    content_error = "Please don't save a your post without some content!"

                else:

                    post = form.save(commit=False)
                    post.author = request.user
                    post.last_edited_date = timezone.now()
                    post.asset_ID_id = asset_id
                    post.save()
                    return redirect(post_detail, asset_id, post.pk)

        else:
            form = BlogPostForm(instance=post)

    args = {
        'errors': errors,
        'asset': the_asset,
        'form': form,
        'content_error': content_error
    }
    args.update(csrf(request))

    return render(request, 'blogpostform.html', args)

@login_required(login_url='/login/')
def delete_blog_post(request, asset_id, id):
    errors = []
    content_error = ""
    form = []
    the_asset = []

    #  first check does the post exist?
    if blog_post_exists(asset_id, id) == False:

        errors.append("This page does not exist")

    else:
        # it does exist
        post = Post.objects.get(id=id, asset_ID_id=asset_id)
        the_asset = get_object_or_404(Asset, pk=asset_id)

        # but now check that this user is allowed to view posts for this asset
        my_id = request.user

        if check_user_linked_to_asset(my_id, asset_id) == False:
            # prepare the error message
            errors.append("You are not authorised to delete this Post")
            # set these to empty
            the_asset = []

        # and finally check if the user is the one who CREATED this post
        # only they should be allowed to delete (or the staff)

        if check_user_linked_to_blog_post(my_id, asset_id, id) == False:
            if not request.user.is_staff:
                messages.error(request, "You are not authorised to delete this Post")
                # set these to empty
                the_asset = []

                return redirect(post_detail, asset_id, id)

        post.delete()

        messages.success(request, "This Blog entry has been deleted")

        return redirect(reverse('post_list', kwargs={"asset_id": asset_id}))