from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import *
from feed.models import Post


def user_reg_view(request):
    """
    User Registration View.
    """
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


def logout_view(request):
    """
    Logout View.
    """
    logout(request)
    return redirect('home')


def login_view(request):
    """
    Login View.
    """
    context = {}

    # Returns already logged in users home if they
    # try to log in.
    user = request.user
    if user.is_authenticated:
        return redirect('home')

    # If someone tries to log in, check if the credentials
    # matches an already registered user. If login is success
    # Redirect home, otherwise back to LoginForm
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
    """
    View for User Profiles.
    """
    context = {}
    # Gets the Account object of the profile that is being loaded,
    # filters post to all their created ones.
    profile = get_object_or_404(Account, username=username)
    context['profile'] = profile
    posts = Post.objects.filter(author=profile)
    context['posts'] = posts

    # This code handles the showing of the Username in the Update Username form
    # that is displayed on the profile page as user settings when you view your
    # own profile, and updating of it.
    if request.POST:
        form = UpdateUsernameForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                'username': request.POST['username'],
            }
        form.save()
        new_username = form.cleaned_data['username']
        context['username'] = new_username
        return redirect('user', username=new_username)
    else:
        form = UpdateUsernameForm(
            initial={
                'username': request.user.username,
            })
    context['username_form'] = form
    return render(request, 'user.html', context)
