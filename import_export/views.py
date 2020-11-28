import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from django.views.generic import FormView, ListView
# Create your views here.
# one parameter named request
from import_export.models import  Email_Dump, DataSheetFromCommonNinja
from accounts.views import send_email_confirmation_link

from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Count


class EmailUpload(FormView):

    def get(self, request, *args, **kwargs):
        """
        docstring
        """
        return render(request, 'import_export/emails_upload.html')

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

            _, created = Email_Dump.objects.update_or_create(
                name=column[0],
                email=column[1],
                vote_time=date_time_obj,
            )
            print(count)

        messages.warning(request, 'message from post function')
        return render(request, 'import_export/emails_upload.html')

# Data Sheet upload - form
class DataSheetUpload(FormView):

    def get(self, request, *args, **kwargs):
        """
        docstring
        """
        return render(request, 'import_export/data_sheet_upload.html')

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
            
            _, created = DataSheetFromCommonNinja.objects.update_or_create(
                name=column[0],
                email=column[1],
                ip_address = column[2], 
                group = column[3], 
                round = column[4], 
                game = column[5],
                voted_for = column[6],
            )
            print(count)

        messages.warning(request, 'message from post function')
        return render(request, 'import_export/data_sheet_upload.html')



# Unique / Email Voter listing
class EmailDumpList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.all()

class VerifiedEmailList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(email_confirmed=True).order_by('email')


class PendingEmailList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(verification_pending=True, email_confirmed=False, invalid=False).order_by('email')

class IsEmailSendList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(verification_pending=True, email_confirmed=False, invalid=False, is_email_sent=False).order_by('email')


class InvalidEmailList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(invalid=True, email_confirmed=False).order_by('email')


# IP Address - linting
# class IPAddressList(ListView):
#     template_name = 'ip_address_list.html'
#     model = DataSheetFromCommonNinja
#     queryset = DataSheetFromCommonNinja.objects.values('ip_address').order_by('ip_address').annotate(the_count=Count('ip_address'))

def ip_address_list(request):
    ip_list = list(DataSheetFromCommonNinja.objects.values("ip_address").order_by('the_count').annotate(the_count=Count('ip_address')))
    # ip_list = [{'ip_address': '100.1.131.190', 'the_count': 4}, {'ip_address': '100.12.91.148', 'the_count': 4},]
    return render(request, 'import_export/ip_address_list.html', context={'object_list': ip_list})

# Data Sheet Copy - linting
class DataSheetListView(ListView):
    model = DataSheetFromCommonNinja
    paginate_by = 10
    queryset = DataSheetFromCommonNinja.objects.all().order_by('name')



def load_unique_emails(request):
    # uni_email_obj = list(DataSheetFromCommonNinja.objects.order_by().values('name', 'email').distinct())
    # uni_email_obj = DataSheetFromCommonNinja.objects.order_by().values( 'email').distinct().count()
    # uni_email_obj = DataSheetFromCommonNinja.objects.values_list('email').distinct()
    uni_email_obj = list(DataSheetFromCommonNinja.objects.all().order_by('email').distinct('email'))


    # print(uni_email_obj)
    
    count = 0
    new_entry = 0
    for uobj in uni_email_obj:
        count = count +1
        # if Email_Dump.objects.get(email=uobj.email):
        #     print('exist')
        # else:
        #     Email_Dump.objects.create(name=uobj.name, email=uobj.email).save()
        #     print('exist')


        _, created = Email_Dump.objects.update_or_create(
            name=uobj.name,
            email=uobj.email)
        print(count)
        if created:
            new_entry = new_entry +1
    
    str_msg = 'New entry '+ str(new_entry)
    messages.success(request, str_msg)
    return redirect('import_export:unique-emails')


class DateWiseEmailList(ListView):
    model = Email_Dump
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
    obj = Email_Dump.objects.get(pk=pk)
    result = send_email_confirmation_link(request, obj, obj.email)
    if result:
        return redirect('import_export:unique-emails')
    
    return redirect('import_export:unique-emails')
