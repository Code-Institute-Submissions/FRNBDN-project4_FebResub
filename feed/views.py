from django.shortcuts import render, get_object_or_404, redirect
from account.models import Account
from django.forms import ModelForm
from django.views import generic, View
from django.http import HttpResponse
from .models import *
from .forms import *


class Feed(generic.ListView):
    model = Post
    queryset = Post.objects.filter(listed=True).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 10


class PostDetail(View):
    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(listed=True)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.all().order_by('-created_on')
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
        comments = post.comments.all().order_by('-created_on')
        liked = False
        disliked = True
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        if post.dislikes.filter(id=self.request.user.id).exists():
            disliked = True

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment_form.instance.commenter = request.user
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
                'comment_form': CommentForm(),
            }
        )


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'edit_post.html', {'form': form, 'create': True})


def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        return HttpResponse('You may only edit posts you have created.')
    else:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.save()
            return redirect('post_detail', slug=post.slug)
        else:
            form = PostForm(instance=post, initial={
                'title': post.title,
                'body': post.body,
                'thumbnail': post.thumbnail,
            }
            )
        return render(request, 'edit_post.html',
                      {'form': form, 'is_create': False})
