from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm, SetPasswordForm
# from django.http import Http404
from django.shortcuts import redirect
from django.contrib import messages

class SignUpForm(UserCreationForm):
    # first_name = forms.CharField(
    #     max_length=50, 
    #     widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'First Name', 'class':'form-control'})
    #     )
    # last_name = forms.CharField(
    #     max_length=50, 
    #     widget=forms.TextInput(attrs={'type':'text', 'placeholder': 'Last Name', 'class':'form-control'})
    #     ) 
    email = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Enter Email', 'class':'form-control'})
        )
    password1 = forms.CharField(    
        max_length=15, 
        widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'Enter Password', 'class':'form-control'})
        )
    password2 = forms.CharField(
        max_length=15, 
        widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'Re-Enter Password', 'class':'form-control'})
        )

    class Meta:
        model = User
        # fields = ('first_name','last_name','email', 'password1', 'password2', )
        fields = ('email', 'password1', 'password2', )


class SignInForm(forms.Form):
    email = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Email Address', 'class':'form-control', 'autofocus':'true'})
        )
    password = forms.CharField(
        max_length=30, 
        widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'Enter Password', 'class':'form-control'})
        )


class EmailValidationOnForgotPassword(PasswordResetForm):
    email = forms.CharField(
        max_length=50, 
        widget=forms.TextInput(attrs={'type':'email', 'placeholder': 'Enter Email', 'class':'form-control'})
        )

    # html_email_template_name = 'users/email/forget_html_email_password.html'
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            # raise ValidationError("There is no user registered with the specified email address!")
            # messages.warning(self.request, 'Invalid email address')
            # raise Http404("Poll does not exist")
            pass
        return email


class PasswordResetConfirmForm(SetPasswordForm):
        new_password1 = forms.CharField(
            max_length=50, 
            widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'Enter new password', 'class':'form-control'})
        )
        new_password2 = forms.CharField(
            max_length=50, 
            widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'New password confirmation', 'class':'form-control'})
        )


class SetNewPasswordForm(PasswordChangeForm):
        old_password = forms.CharField(
            max_length=50, 
            widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'Enter old password', 'class':'form-control'})
        )
        new_password1 = forms.CharField(
            max_length=50, 
            widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'Enter new password', 'class':'form-control'})
        )
        new_password2 = forms.CharField(
            max_length=50, 
            widget=forms.TextInput(attrs={'type':'password', 'placeholder': 'New password confirmation', 'class':'form-control'})
        )