import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from django.views.generic import FormView, ListView
# Create your views here.
# one parameter named request
from import_export.models import Profile, Email_Dump, DataSheetFromCommonNinja
from accounts.views import send_email_confirmation_link

from datetime import datetime
from django.utils.timezone import make_aware

def profile_upload(request):
    # declaring template
    template = "import_export/profile_upload.html"
    data = Profile.objects.all()
    # prompt is a context variable that can have different values      depending on their context
    prompt = {
        'order': 'Order of the CSV should be name, email, address,    phone, profile',
        'profiles': data    
            }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)

    csv_file = request.FILES['file']
    # let's check if it is a csv file
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'THIS IS NOT A CSV FILE')

    data_set = csv_file.read().decode('UTF-8')
    print(data_set)

    # setup a stream which is when we loop through each line we are able to handle a data in a stream
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = Profile.objects.update_or_create(
            name=column[0],
            email=column[1],
            address=column[2],
            phone=column[3],
            profile=column[4]
        )
    context = {}
    return render(request, template, context)


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
            
            str_date = column[7][0:24]
            try:
                # str_date = "Nov 23 2020 16:19:41" # example
                date_time_obj = datetime.strptime(str_date, "%a %b %d %Y %H:%M:%S")
                aware_datetime = make_aware(date_time_obj)
                # date_time_obj = "2012-09-04 06:00Z" # example
            except ValueError as e:
                date_time_obj = datetime.strptime(str_date, "%a %b %d %Y %H:%M:")

            _, created = DataSheetFromCommonNinja.objects.update_or_create(
                name=column[0],
                email=column[1],
                ip_address = column[2], 
                group = column[3], 
                round = column[4], 
                game = column[5],
                voted_for = column[6],
                date = aware_datetime
            )
            print(count)

        messages.warning(request, 'message from post function')
        return render(request, 'import_export/data_sheet_upload.html')


class EmailDumpList(ListView):
    model = Email_Dump
    paginate_by = 10


class VarifiedEmailList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(email_confirmed=True).order_by('email')


class PendingEmailList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(varification_pending=True, email_confirmed=False, invalid=False).order_by('email')

class InvalidEmailList(ListView):
    model = Email_Dump
    paginate_by = 10
    queryset = Email_Dump.objects.filter(invalid=True, email_confirmed=False).order_by('email')

class DataSheetListView(ListView):
    model = DataSheetFromCommonNinja
    paginate_by = 10
    queryset = DataSheetFromCommonNinja.objects.all().order_by('name')


def load_unique_emails(request):
    uni_email_obj = list(DataSheetFromCommonNinja.objects.order_by().values('name', 'email', 'date').distinct())
    count = 0
    for uobj in uni_email_obj:
        count = count +1
        _, created = Email_Dump.objects.update_or_create(
            name=uobj['name'],
            email=uobj['email'], 
            vote_time=uobj['date'])
        print(count)
        # str_msg = 'New entry'
        # messages.success(request, str_msg)
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
