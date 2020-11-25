from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView, 
    PasswordResetConfirmView, PasswordResetCompleteView,
    LogoutView
)

from .forms import EmailValidationOnForgotPassword, PasswordResetConfirmForm
from .views import LoginView, RegisterView, ForgetPasswordView, ChangePasswordView
from .import views

app_name = 'accounts'

urlpatterns = [

    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

    re_path(r'^email-activate/(?P<oidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.email_activate, name='email_activate'),
    

    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'), 

    
    # path('password/reset/', ForgetPasswordView.as_view(), name='forget_password'),
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),


    path('password/reset/',
        PasswordResetView.as_view(
            template_name='accounts/password_reset_form.html',
            form_class=EmailValidationOnForgotPassword,
            html_email_template_name = 'accounts/email/forget_password_email.html'
            ), 
        name='password_reset'
        ),

    path('password/reset/done/', PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),

    path('password/reset/confirm/<uidb64>[0-9A-Za-z]+)-<token>/',
        PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            form_class=PasswordResetConfirmForm), 
            name='password_reset_confirm'
        ),

    path('password/reset/complete/', 
        PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'),
            name='password_reset_complete'
        ),
    
]

