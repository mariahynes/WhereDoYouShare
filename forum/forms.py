from django import forms
from .models import Thread, Post

class ThreadForm(forms.ModelForm):

    name = forms.CharField(label="New Thread Name")

    class Meta:
        model = Thread
        fields = ['name']


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['comment']

