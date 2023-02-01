from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
from django_summernote.fields import SummernoteTextField


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'thumbnail']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body', 'parent']
