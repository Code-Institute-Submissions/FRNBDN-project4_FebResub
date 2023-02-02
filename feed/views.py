from django.shortcuts import render, get_object_or_404, redirect, reverse
from account.models import Account
from django.forms import ModelForm
from django.views import generic, View
from django.http import HttpResponse, HttpResponseRedirect
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
        comments = Comment.objects.filter(post=post).order_by('-created_on')   
        liked = False
        disliked = False
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
        if self.request.method == 'POST':
            comment_form = CommentForm(self.request.POST)
            if comment_form.is_valid():
                body = comment_form.cleaned_data['body']
                try:
                    parent = comment_form.cleaned_data['parent']
                except NoParent:
                    parent = None

            new_comment = Comment(
                body=body,
                commenter=self.request.user,
                post=post,
                parent=parent)
            new_comment.save()
            return redirect('post_detail', slug=post.slug)


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

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
        return redirect('post_detail', slug=post.slug)

    form = PostForm(instance=post, initial={
        'title': post.title,
        'body': post.body,
        'thumbnail': post.thumbnail,
    }
    )
    return render(request, 'edit_post.html',
                  {'form': form, 'is_create': False})


class PostLike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)

        elif post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
            post.likes.add(request.user)

        else:
            post.likes.add(request.user)

        return redirect('post_detail', slug=slug)


class PostDislike(View):

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            post.dislikes.add(request.user)

        elif post.dislikes.filter(id=request.user.id).exists():
            post.dislikes.remove(request.user)
        else:
            post.dislikes.add(request.user)

        return redirect('post_detail', slug=slug)


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = "/"
    template_name = "post_confirm_delete.html"


class CommentDeleteView(generic.DeleteView):
    model = Comment
    template_name = "comment_confirm_delete.html"

    def get_success_url(self):
        return redirect('post_detail', slug=self.object.post.slug)


class EditCommentView(generic.UpdateView):
    model = Comment
    fields = ['body']
    template_name = 'edit_comment.html'

    def get_success_url(self):
        return redirect('post_detail', slug=self.object.post.slug)
