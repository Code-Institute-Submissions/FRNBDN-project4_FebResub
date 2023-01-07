from django.shortcuts import render, get_object_or_404, redirect
from account.models import Account
from django.forms import ModelForm
from django.views import generic, View
from django.http import HttpResponse
from .models import *
from .forms import PostForm, CommentForm


class Feed(generic.ListView):
    model = Post
    queryset = Post.objects.filter(listed=True).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 200


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(listed=True)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.all().order_by('created_on')
        liked = False
        disliked = True
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if post.dislikes.filter(id=self.request.user.id).exists():
            disliked = True

        return render(
            request,
            'post_detail.html',
            {
                'post': post,
                'comments': comments,
                'liked': liked,
                'disliked': disliked,
                'comment_form': CommentForm()
            }
        )

        def post(self, request, slug, *args, **kwargs):
            queryset = Post.objects.filter(listed=True)
            post = get_object_or_404(queryset, slug=slug)
            comments = post.comments.all().order_by('created_on')
            liked = False
            disliked = True
            if post.likes.filter(id=self.request.user.id).exists():
                liked = True
            if post.dislikes.filter(id=self.request.user.id).exists():
                disliked = True

            comment_form = CommentForm(data=request.POST)

            if comment_form.is_valid():
                comment_form.instance.commenter = request.user.username
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.save()
            else:
                comment_form = CommentForm()

            return render(
                request,
                'post_detail.html',
                {
                    'post': post,
                    'comments': comments,
                    'liked': liked,
                    'disliked': disliked,
                    'comment_form': CommentForm()
                }
            )


class CreatePost(View):

    def get(self, request, *args, **kwargs):

        return render(
            request,
            'edit_post.html',
            {
                'form': PostForm(),
            }
        )
    
    def post(self, request, *args, **kwargs):

        form = PostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.instance.save(commit=False)
            post.author = Account.objects.filter(
                    email=request.user.email).first()
            post.save()
            form = PostForm()
        else:
            form = PostForm()

        return render(
            request,
            'edit_post.html',
            {
                'form': PostForm(),
            }
        )

