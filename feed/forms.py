from django import forms
from .models import Post, Comment
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'thumbnail']
        widgets = {
            'body': SummernoteWidget(attrs={'width': '20%'}),
            'thumbnail': forms.FileInput(attrs={'accept': 'image/*'}),
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body', 'parent']
