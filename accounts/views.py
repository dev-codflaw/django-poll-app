from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
import random
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import SignUpForm, SignInForm
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail

from .tokens import account_activation_token


from django.contrib.auth import login, authenticate
# from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
# models
from accounts.models import User
from django.contrib.auth.hashers import check_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.mixins import LoginRequiredMixin



class Hello(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'hello.html')

class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = SignInForm(request.POST)
            return render(request, 'accounts/login.html', {'form': form})
            
    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        email = request.POST['email']
        raw_password = request.POST['password']
        if User.objects.filter(email=email).exists():
            # messages.warning(request, 'User exists')
            try:
                usr_obj = User.objects.get(email=email)
                if check_password(raw_password, usr_obj.password):
                    # messages.success(request, "Valid Credetials")
                    user = authenticate(username=usr_obj.username, password=raw_password)
                    if user is not None:    
                        # messages.warning(request,'User Authenticated!' )
                        login(request, user)
                        return redirect('home')
                    else:
                        messages.warning(request,'User Not Authenticated! Please varify the Email!' )
                else:
                    messages.warning(request, "Invalid Credetials")
            except Exception as e:
                messages.warning(request, e)
        else:
            messages.warning(request, 'No such user exist, Please register!')
        return render(request, 'accounts/login.html', {'form': form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            form = SignUpForm(request.POST)
            return render(request, 'accounts/register.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.email_confirmed = True
            user.save()
            return redirect('home')

            """ Below code for email activation """
            """
            current_site = get_current_site(request)
            subject = 'Email varification for '+ current_site.name
            html_content = render_to_string('accounts/email/account_activation_email.html',
            {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            }
            )
            text_content = strip_tags(html_content) 
            try:
                msg = EmailMultiAlternatives(subject, text_content, 'ujangid0@gmail.com', [request.POST.get('email')])
                msg.attach_alternative(html_content, "text/html")
                msg.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.warning(request, 'Account activation link sent on email, Please Check!')
            return redirect('login')
            """
        else:
            messages.warning(request, form.errors)
            return render(request, 'accounts/register.html', {'form':form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        context = {'text_msg':'Congrats! Your email address is confirmed!'}
        return render(request, 'accounts/simple_message_page.html', context)
        # login(request, user)
        # return redirect('home')
    else:
        context = {'text_msg':'The confirmation link was invalid, possibly because it has already been used.'}
        return render(request, 'accounts/simple_message_page.html', context)
