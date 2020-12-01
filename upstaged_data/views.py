import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from django.views.generic import FormView, ListView
# Create your views here.
# one parameter named request
from upstaged_data.models import  Voter, Datasheet
from accounts.views import send_email_confirmation_link

from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Count


class EmailUpload(FormView):

    def get(self, request, *args, **kwargs):
        """
        docstring
        """
        return render(request, 'upstaged_data/emails_upload.html')

    def post(self, request, *args, **kwargs):
        """
        docstring
        """
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')  

        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        count = 0


        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            count = count + 1
            str_date = column[7].strip('GMT+0000 (Coordinated Universal Time)')

            try:
                # str_date = "Nov 23 2020 16:19:41" # example
                date_time_obj = datetime.strptime(str_date, "%b %d %Y %H:%M:%S")
                # date_time_obj = "2012-09-04 06:00Z" # example
            except ValueError as e:
                date_time_obj = datetime.strptime(str_date, "%b %d %Y %H:%M:")

            _, created = Voter.objects.update_or_create(
                name=column[0],
                email=column[1],
                vote_time=date_time_obj,
            )
            print(count)

        messages.warning(request, 'message from post function')
        return render(request, 'upstaged_data/emails_upload.html')


# Data Sheet upload - form
class DataSheetUpload(FormView):

    def get(self, request, *args, **kwargs):
        """
        docstring
        """
        return render(request, 'upstaged_data/data_sheet_upload.html')

    def post(self, request, *args, **kwargs):
        """
        docstring
        """
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')  

        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        create_count = 0
        skip_count = 0
        for column in csv.reader(io_string, delimiter=',', quotechar="|"): 
            if not Datasheet.objects.filter(name=column[0].strip(), email=column[1], game=column[5]).exists():
                Datasheet.objects.create(
                    name = column[0].strip(),
                    email = column[1].strip(),
                    ip_address = column[2].strip(),
                    group = column[3].strip(),
                    round = column[4].strip(),
                    game = column[5].strip(),
                    voted_for = column[6].strip(),
                    vote_time = column[7].strip(),
                )
                create_count = create_count + 1
            else:
                skip_count = skip_count + 1

        print(create_count)
        print(skip_count)

        messages.warning(request, 'message from post function')
        return render(request, 'upstaged_data/data_sheet_upload.html')



# Unique / Email Voter listing
class VoterList(ListView):
    model = Voter
    paginate_by = 10
    queryset = Voter.objects.all()

class VerifiedEmailList(ListView):
    model = Voter
    paginate_by = 10
    queryset = Voter.objects.filter(email_confirmed=True).order_by('email')


class PendingEmailList(ListView):
    model = Voter
    paginate_by = 10
    queryset = Voter.objects.filter(verification_pending=True, email_confirmed=False, invalid=False).order_by('email')

class IsEmailSendList(ListView):
    model = Voter
    paginate_by = 10
    queryset = Voter.objects.filter(verification_pending=True, email_confirmed=False, invalid=False, is_email_sent=False).order_by('email')


class InvalidEmailList(ListView):
    model = Voter
    paginate_by = 10
    queryset = Voter.objects.filter(invalid=True, email_confirmed=False).order_by('email')


# IP Address - linting
# class IPAddressList(ListView):
#     template_name = 'ip_address_list.html'
#     model = Datasheet
#     queryset = Datasheet.objects.values('ip_address').order_by('ip_address').annotate(the_count=Count('ip_address'))

def ip_address_list(request):
    ip_list = list(Datasheet.objects.values("ip_address").order_by('the_count').annotate(the_count=Count('ip_address')))
    # ip_list = [{'ip_address': '100.1.131.190', 'the_count': 4}, {'ip_address': '100.12.91.148', 'the_count': 4},]
    return render(request, 'upstaged_data/ip_address_list.html', context={'object_list': ip_list})

# Data Sheet Copy - linting
class DataSheetListView(ListView):
    model = Datasheet
    paginate_by = 10
    queryset = Datasheet.objects.all().order_by('name')



def load_unique_emails(request):
    uni_email_obj = list(Datasheet.objects.all().order_by('email').distinct('email'))
    # print(uni_email_obj)
    skip_count = 0
    new_entry = 0
    for uobj in uni_email_obj:
        if not Voter.objects.filter(email=uobj.email).exists():
            Voter.objects.create(
                name=uobj.name,
                email=uobj.email,
            )
            new_entry = new_entry +1
        else:
            skip_count = skip_count +1

        # _, created = Voter.objects.update_or_create(
        #     name=uobj.name,
        #     email=uobj.email)
            
    
    str_msg = 'New entry '+ str(new_entry)
    str_msg = 'Skip entry '+ str(skip_count)
    messages.success(request, str_msg)
    return redirect('upstaged_data:unique-emails')


class DateWiseEmailList(ListView):
    model = Voter
    paginate_by = 10
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            # When pagination is enabled and object_list is a queryset,
            # it's better to do a cheap query than to load the unpaginated
            # queryset in memory.
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, 'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = not self.object_list
            if is_empty:
                raise Http404(_("Empty list and '%(class_name)s.allow_empty' is False.") % {
                    'class_name': self.__class__.__name__,
                })
        fromDate = request.GET['fromDate']
        toDate = request.GET['toDate']
        
        context = self.get_context_data(fromDate=fromDate, toDate=toDate)
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, fromDate, toDate,  **kwargs):
        """Get the context for this view."""

        context = {
            'fromDate': fromDate,
            'toDate': toDate,

        }
        
        context.update(kwargs)
        return super().get_context_data(**context)

    

    
def send_email_confirmation(request, pk):
    obj = Voter.objects.get(pk=pk)
    result = send_email_confirmation_link(request, obj, obj.email)
    if result:
        return redirect('upstaged_data:unique-emails')
    
    return redirect('upstaged_data:unique-emails')
