from django import forms
from .models import Post

class BlogPostForm(forms.ModelForm):

    image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ('title', 'content', 'image')
