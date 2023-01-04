from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')


class LoginForm(forms.ModelForm):

    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Email & Password doesn't match")


class UpdateUsernameForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('username', )

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(
                                                     username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already taken'
                                    % account.username)