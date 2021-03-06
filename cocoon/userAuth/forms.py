from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.db import transaction
from .models import MyUser, UserProfile
from django import forms
from cocoon.signature.models import HunterDocManagerModel
import re

from .constants import BROKER_CREATION_KEY
from .helpers.send_verification_email import send_verification_email


# Load the logger
import logging
logger = logging.getLogger(__name__)


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


class BaseRegisterForm(UserCreationForm):

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

    phone_number = forms.CharField(
        required=False,
        label="Phone number",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please use format: ##########',
                'pattern': '\d{10}',
            }
        )
    )

    def is_valid(self):
        valid = super(BaseRegisterForm, self).is_valid()

        if not valid:
            return valid

        current_form = self.cleaned_data.copy()

        # makes sure that the phone number is formatted properly
        if current_form['phone_number']:
            pattern = re.compile("^(\d{3}[\-]\d{3}[\-]\d{4})$")
            pattern1 = re.compile("^\d{10}")
            if not pattern.match(current_form['phone_number']) and not pattern1.match(current_form['phone_number']):
                valid = False
                self.add_error('phone_number', "Phone number not in valid format")

        return valid

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'phone_number',]


class ApartmentHunterSignupForm(BaseRegisterForm):

    agent_referral = forms.CharField(
        required=False,
        label="Agent Referral",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Agent Referral - Optional',
            }
        )
    )

    def is_valid(self):
        valid = super(BaseRegisterForm, self).is_valid()

        if not valid:
            return valid

        current_form = self.cleaned_data.copy()

        # makes sure that the phone number is formatted properly
        if current_form['agent_referral']:
            if not UserProfile.objects.filter(url=current_form['agent_referral'], user__is_broker=True).exists():
                valid = False
                self.add_error('agent_referral', "Agent URL not valid, please contact your agent to verify your URL")
            elif UserProfile.objects.filter(url=current_form['agent_referral']).count() != 1:
                valid = False
                self.add_error('agent_referral', "More than one agent exists, please contact support for help via "
                                                 "intercom in the bottom right")
                logger.error("More than one agent returned for agent referral: {0}".format(current_form['agent_referral']))
        return valid

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.is_hunter = True
        user.is_verified = False
        user.save()

        if self.cleaned_data['agent_referral']:
            try:
                user.userProfile.referred_agent = UserProfile.objects.get(url=self.cleaned_data['agent_referral']).user
                user.userProfile.save()
            except UserProfile.MultipleObjectsReturned:
                logger.error("Error in agent sign up form, multiple agents returned: {0}".format(self.cleaned_data['agent_referral']))
            except UserProfile.DoesNotExist:
                pass

        domain = kwargs.pop('request', None)
        send_verification_email(domain, user)

        HunterDocManagerModel.objects.get_or_create(user=user)
        return user


class BrokerSignupForm(BaseRegisterForm):

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

    def is_valid(self):
        valid = super(BrokerSignupForm, self).is_valid()

        if not valid:
            return valid

        current_form = self.cleaned_data.copy()

        if current_form['creation_key'] != BROKER_CREATION_KEY:
            self.add_error('creation_key', "Creation Key invaild")
            valid = False

        return valid

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

    @transaction.atomic
    def save(self, **kwargs):
        user = super().save(commit=False)
        user.is_broker = True
        user.is_verified = False
        user.save()

        domain = kwargs.pop('request', None)
        send_verification_email(domain, user)

        HunterDocManagerModel.objects.get_or_create(user=user)
        return user


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
        fields = ['email', 'first_name', 'last_name']
