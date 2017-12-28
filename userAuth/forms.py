# Import django modules
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

# Import userAuth models
from .models import MyUser


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Username',
            }),
    )
    password = forms.CharField(
        label="Password",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'password',
                'placeholder': 'Password',
                'type': 'password',
            }),
    )
    remember = forms.BooleanField(
        label="Remember",
        initial=False,
        required=False,
    )


class RegisterForm(UserCreationForm):

    creation_key = forms.CharField(
        required=True,
        label="Please enter the key",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'key',
            }
        )
    )

    email = forms.EmailField(
        required=True,
        label="Email Address",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Username',
            }),
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        ),
    )

    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'password',
            }
        ),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    first_name = forms.CharField(
        required=True,
        label="First name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'first name',
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="Last name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'last name',
            }
        )
    )

    class Meta:
        model = MyUser
        fields = ["email_user", "first_name_user", "last_name_user", 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        label="Email Address",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'name': 'username',
            }),
        required=False,
    )
    first_name = forms.CharField(
        required=True,
        label="First name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'first name',
            }
        )
    )
    last_name = forms.CharField(
        required=True,
        label="Last name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'last name',
            }
        )
    )

    class Meta:
        model = MyUser
        fields = ["email_user", "first_name_user", "last_name_user"]
