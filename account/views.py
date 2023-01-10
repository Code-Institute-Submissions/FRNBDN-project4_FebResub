from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import *
from feed.models import Post


# User Registration View
def user_reg_view(request):
    context = {}
    if request.POST:
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            set_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=set_password)
            login(request, account)
            return redirect('home')
        else:
            context['user_reg_form'] = form
    else:
        form = UserRegistrationForm()
        context['user_reg_form'] = form
    return render(request, 'register.html', context)


# Logout View
def logout_view(request):
    logout(request)
    return redirect('home')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('home')
    
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    
    context['login_form'] = form
    return render(request, 'login.html', context)


def user_view(request, username):
    context = {}
    
    profile = get_object_or_404(Account, username=username)
    context['profile'] = profile
    posts = Post.objects.filter(author=profile)
    context['posts'] = posts

    if request.POST:
        form = UpdateUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                'username': request.POST['username'],
                }  
        form.save()
        context['success_message'] = 'Updated!'
    else:
        form = UpdateUsernameForm(
            initial={
                'username': request.user.username,
            })       
    context['username_form'] = form
    return render(request, 'user.html', context)