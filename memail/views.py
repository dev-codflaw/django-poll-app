from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
# Create your views here.
from django.views.generic import TemplateView, FormView, UpdateView, DetailView
from django.contrib import messages
from import_export.models import Email_Dump
from PIL import Image
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.utils.html import strip_tags
from django.urls import reverse

from app.mail_crd import EMAIL_HOST_USER

class SimpleEmailView(FormView):
    success_url = '/memail/'

    def get(self, request, *args, **kwargs):
        print('get')
        return render(request, 'memail/single_email.html')

    def post(self, request, *args, **kwargs):
        subject = request.POST['subject']
        email_msg = request.POST['email-msg']
        to_email = request.POST['to-email'] 

        # using template to generate the email content
        template = get_template("memail/email.html")
        context_data = dict()

        # pass the variable image_url to template
        # image_load is the URL name. see below
        context_data["image_url"] = request.build_absolute_uri(reverse('memail:image_load'))
        html_text = template.render(context_data)
        plain_text = strip_tags(html_text)

        try:
            from_email = EMAIL_HOST_USER
        except Exception as e:
            messages.warning(request, e)
        try:
            msg = EmailMultiAlternatives(subject, plain_text, 'UltimateOctet NCPA <arun.sharma@upstagedu.com>', [to_email])
            msg.attach_alternative(html_text, "text/html")
            msg.send()
            # send_mail(subject, email_msg, 'ujangid0@gmail.com', [to_email], fail_silently=False)
            messages.success(request, 'Email sent to '+to_email)
        except Exception as e:
            messages.warning(request, e)

        # self.form_valid(request)
        return render(request, 'memail/single_email.html')
    
    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        print(form)
        print('form-valid')
        return HttpResponseRedirect(self.get_success_url())        
    
    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print('form-invalid')
        return self.render_to_response(self.get_context_data(form=form))



def image_load(request):
    print("\nImage Loaded\n")
    red = Image.new('RGB', (1, 1))
    response = HttpResponse(content_type="image/png")
    red.save(response, "PNG")
    
    return response

