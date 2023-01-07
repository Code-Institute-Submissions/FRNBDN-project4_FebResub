from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'thumbnail']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body', ]


class UpdatePostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'body', 'thumbnail']

    def save(self, commit=True):
        post = self.instance
        post.title = self.cleaned_data['title']
        post.body = self.cleaned_data['body']

        if self.cleaned_data['thumbnail']:
            post.thumbnail = self.cleaned_data['thumbnail']
        if commit:
            post.save()
        return post