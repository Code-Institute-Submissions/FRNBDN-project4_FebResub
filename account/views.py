from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from account.forms import UserRegistrationForm


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