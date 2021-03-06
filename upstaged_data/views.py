import csv, io
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from django.views.generic import FormView, ListView
# Create your views here.
# one parameter named request
from upstaged_data.models import  Voter, Datasheet, TempDatasheet, DuplicateVotes, TempVoter
from accounts.views import send_email_confirmation_link

from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Count
from upstaged_data.resources import VoterResource
from django.db import connection

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
        fake_entry = []
        for column in csv.reader(io_string, delimiter=',', quotechar="|"): 
            if not Datasheet.objects.filter(email=column[1].strip(), game=column[5].strip()).exists():
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
                # print(create_count)
            else:
                skip_count = skip_count + 1
                # print(skip_count)

        # print(create_count)
        # print(skip_count)
        messages.warning(request, 'message from post function')
        return render(request, 'upstaged_data/data_sheet_upload.html')


# Data Sheet upload - form - find duplicate entry
class DuplicateDataSheetFind(FormView):
    def get(self, request, *args, **kwargs):
        return render(request, 'upstaged_data/duplicate_votes_list.html')
    
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'THIS IS NOT A CSV FILE')  
        data_set = csv_file.read().decode('UTF-8')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        create_count = 0
        fake_entry = []
        fake_entry_count = 0
        for column in csv.reader(io_string, delimiter=',', quotechar="|"): 
            if not TempDatasheet.objects.filter(email=column[1].strip(), game=column[5].strip()).exists():
                TempDatasheet.objects.create(
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
                # print(create_count)
            elif not DuplicateVotes.objects.filter(name=column[0].strip(), email=column[1].strip(), game=column[5].strip(), voted_for=column[6].strip()).exists():
                print(column[1])
                DuplicateVotes.objects.create(
                    name = column[0].strip(),
                    email = column[1].strip(),
                    ip_address = column[2].strip(),
                    group = column[3].strip(),
                    round = column[4].strip(),
                    game = column[5].strip(),
                    voted_for = column[6].strip(),
                    vote_time = column[7].strip(),               
                )
                fake_entry_count = fake_entry_count + 1
                # print(fake_entry_count)
            else:
                pass
        TempDatasheet.objects.all().delete()      
        # print(create_count)
        # print(fake_entry_count)
        return render(request, 'upstaged_data/duplicate_votes_list.html')


# script for finding duplicate entry from common ninja datasheet - clean entry from beginning to end
def export_dulicate_entry(request):

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    #Header
    writer.writerow(['Name', 'Email', 'IP Address', 'Group', 'Round', 'Game', 'Voted For', 'Date'])
    obj_list = []
    res_list = DuplicateVotes.objects.all()
    for ob in res_list:
        obj_list.append([ob.name, ob.email, ob.ip_address, ob.group, ob.round, ob.game, ob.voted_for, ob.vote_time,])
    #CSV Data
    writer.writerows(obj_list)
    response['Content-Disposition'] = 'attachment; filename="fakevoters.csv"'
    return response

def export_all_invalid_voters(request):
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    #Header
    writer.writerow(['Name', 'Email', 'IP Address', 'Group', 'Round', 'Game', 'Voted For', 'Date'])
    obj_list = []
    res_list = DuplicateVotes.objects.all()
    for ob in res_list:
        obj_list.append([ob.name, ob.email, ob.ip_address, ob.group, ob.round, ob.game, ob.voted_for, ob.vote_time,])
    #CSV Data
    writer.writerows(obj_list)
    response['Content-Disposition'] = 'attachment; filename="fakevoters.csv"'
    return response

class DuplicateVoteList(ListView):
    model = DuplicateVotes
    paginate_by = 10

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

    def get_context_data(self, **kwargs):
        context = super(InvalidEmailList, self).get_context_data(**kwargs)
        context['page_url_invalid_tag'] = '/voter/invalid/'
        return context

class IPVoterAction(ListView):

    def get(self, request, *args, **kwargs):
        # print(request.GET['ip'])
        return render(request, 'upstaged_data/ip_voter_list.html')

    def post(self, request, *args, **kwargs):
        # print(request.POST['v_action'])
        # print(request.POST['voter_email'])
        # messages.warning(request, 'Test message')
        if request.POST['v_action'] == 'valid':
            valid_act = True
            invalid_act = False
        if request.POST['v_action'] == 'invalid':
            valid_act = False
            invalid_act = True
        action_source = 'by User - '+str(request.user.email)
        # print(action_source)
        # print(valid_act)
        # print(invalid_act)
        Voter.objects.filter(email=request.POST['voter_email']).update(email_confirmed=valid_act, invalid=invalid_act, verification_pending=False, email_verification_source=action_source)
        return redirect('upstaged_data:ip-address-list')

class IPVoterList(ListView):
    template_name = 'upstaged_data/ip_voter_list.html'
    model = Datasheet
    # queryset = Datasheet.objects.values('email', 'ip_address').distinct().filter(ip_address='98.200.166.91')

    def get(self, request, *args, **kwargs):
        print(request.GET['ip'])
        return render(request, 'upstaged_data/ip_voter_list.html')

    def post(self, request, *args, **kwargs):
        # print(request.POST['ip'])
        # queryset = Datasheet.objects.filter(ip_address=request.POST['ip']).order_by('email').distinct('email')
        queryset = Datasheet.objects.values('email').distinct().filter(ip_address=request.POST['ip'])
        # print(list(queryset))
        v = []
        voter_valid_count = 0
        voter_invalid_count = 0
        voter_pending_count = 0
        for vo in queryset:
            # print(vo['email'])
            vtr_obj = list(Voter.objects.filter(email=vo['email']))
            if vtr_obj[0].email_confirmed:
                voter_valid_count = voter_valid_count + 1
            elif vtr_obj[0].invalid:
                voter_invalid_count = voter_invalid_count +1
            elif vtr_obj[0].verification_pending:
                voter_pending_count = voter_pending_count+1
            else:
                print('N/A')
                pass
            # print(vtr_obj[0].email_confirmed)
            v.extend(vtr_obj)
        # print(v)
        valid_prcnt = (voter_valid_count/(voter_valid_count+voter_invalid_count+voter_pending_count))*100
        invalid_prcnt = (voter_invalid_count/(voter_valid_count+voter_invalid_count+voter_pending_count))*100
        pending_prcnt = (voter_pending_count/(voter_valid_count+voter_invalid_count+voter_pending_count))*100
        return render(request, 'upstaged_data/ip_voter_list.html', 
        context={
            'object_list': v,
            'voter_valid_count':voter_valid_count,
            'voter_invalid_count':voter_invalid_count,
            'voter_pending_count':voter_pending_count,
            'valid_prcnt':valid_prcnt,
            'invalid_prcnt':invalid_prcnt,
            'pending_prcnt':pending_prcnt,
            })

# IP Address - listing
class IPAddressList(ListView):
    template_name = 'upstaged_data/ip_address_list.html'
    model = Datasheet
    queryset = Datasheet.objects.values('ip_address').annotate(Count('ip_address')).order_by('ip_address__count').filter(ip_address__count__gt=4)

    def post(self, request, *args, **kwargs):
        num = int(request.POST['num'])
        print(num)
        queryset = Datasheet.objects.values('ip_address',).annotate(Count('ip_address')).order_by('ip_address__count').filter(ip_address__count__gt=num)
        return render(request, 'upstaged_data/ip_address_list.html', context={'object_list': queryset})




class TempIPVoterAction(ListView):

    def get(self, request, *args, **kwargs):
        # print(request.GET['ip'])
        return render(request, 'upstaged_data/temp_ip_voter_list.html')

    def post(self, request, *args, **kwargs):
        # print(request.POST['v_action'])
        # print(request.POST['voter_email'])
        # messages.warning(request, 'Test message')
        if request.POST['v_action'] == 'valid':
            valid_act = True
            invalid_act = False
        if request.POST['v_action'] == 'invalid':
            valid_act = False
            invalid_act = True
        action_source = 'by User - '+str(request.user.email)
        # print(action_source)
        # print(valid_act)
        # print(invalid_act)
        TempVoter.objects.filter(email=request.POST['voter_email']).update(email_confirmed=valid_act, invalid=invalid_act, verification_pending=False, email_verification_source=action_source)
        return redirect('upstaged_data:temp-ip-address-list')

class TempIPVoterList(ListView):
    template_name = 'upstaged_data/temp_ip_voter_list.html'
    model = Datasheet
    # queryset = Datasheet.objects.values('email', 'ip_address').distinct().filter(ip_address='98.200.166.91')

    def get(self, request, *args, **kwargs):
        print(request.GET['ip'])
        return render(request, 'upstaged_data/temp_ip_voter_list.html')

    def post(self, request, *args, **kwargs):
        # print(request.POST['ip'])
        # queryset = Datasheet.objects.filter(ip_address=request.POST['ip']).order_by('email').distinct('email')
        queryset = Datasheet.objects.values('email').distinct().filter(ip_address=request.POST['ip'])
        # print(list(queryset))
        v = []
        voter_valid_count = 0
        voter_invalid_count = 0
        voter_pending_count = 0
        for vo in queryset:
            # print(vo['email'])
            vtr_obj = list(TempVoter.objects.filter(email=vo['email']))
            if vtr_obj[0].email_confirmed:
                voter_valid_count = voter_valid_count + 1
            elif vtr_obj[0].invalid:
                voter_invalid_count = voter_invalid_count +1
            elif vtr_obj[0].verification_pending:
                voter_pending_count = voter_pending_count+1
            else:
                print('N/A')
                pass
            # print(vtr_obj[0].email_confirmed)
            v.extend(vtr_obj)
        # print(v)
        valid_prcnt = (voter_valid_count/(voter_valid_count+voter_invalid_count+voter_pending_count))*100
        invalid_prcnt = (voter_invalid_count/(voter_valid_count+voter_invalid_count+voter_pending_count))*100
        pending_prcnt = (voter_pending_count/(voter_valid_count+voter_invalid_count+voter_pending_count))*100
        return render(request, 'upstaged_data/temp_ip_voter_list.html', 
        context={
            'object_list': v,
            'voter_valid_count':voter_valid_count,
            'voter_invalid_count':voter_invalid_count,
            'voter_pending_count':voter_pending_count,
            'valid_prcnt':valid_prcnt,
            'invalid_prcnt':invalid_prcnt,
            'pending_prcnt':pending_prcnt,
            })


def make_invalid_action_for_ip_voters(request):
    if request.method == 'POST':
        queryset = Datasheet.objects.values('email').distinct().filter(ip_address=request.POST['ip'])
        for vo in queryset:
            # print(vo['email'])
            s = TempVoter.objects.filter(email=vo['email'], verification_pending=True).update(email_confirmed=False, verification_pending=False, invalid=True)
            print(s)
    return redirect('upstaged_data:temp-ip-address-list')

# IP Address - listing
class TempIPAddressList(ListView):
    template_name = 'upstaged_data/temp_ip_address_list.html'
    model = Datasheet
    queryset = Datasheet.objects.values('ip_address').annotate(Count('ip_address')).order_by('ip_address__count').filter(ip_address__count__gt=4)

    def post(self, request, *args, **kwargs):
        num = int(request.POST['num'])
        print(num)
        queryset = Datasheet.objects.values('ip_address',).annotate(Count('ip_address')).order_by('ip_address__count').filter(ip_address__count__gt=num)
        return render(request, 'upstaged_data/temp_ip_address_list.html', context={'object_list': queryset})





def export_voters_datas(request): # not active 
    voter_resource = VoterResource()
    dataset = voter_resource.export()
    # dataset.csv
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="voters.csv"'
    return response
    # return redirect( 'upstaged_data:unique-emails')


# To export all voters data according their status

# def export_voters_data(request):
#     # query_set = "Datasheet.objects.all()"
#     p = "SELECT * FROM datasheet JOIN voter ON datasheet.email = voter.email"
#     cursor = connection.cursor()
#     cursor.execute(p)
#     query_set = cursor.fetchall()
#     # print(query_set)
#     output = []
#     response = HttpResponse (content_type='text/csv')
#     writer = csv.writer(response)
#     #Header
#     writer.writerow(['Name', 'Email', 'IP Address', 'Group', 'Round','Game', 'Voted For', 'Status'])
#     for user in query_set:
#         if user[15]:
#             status = 'Valid'
#         elif user[14]:
#             status = 'Invalid'
#         elif user[16]:
#             status = 'Pending'
#         else:
#             status = 'Not Available'
#         output.append([user[1], user[2], user[3], user[4], user[5], user[6], user[7], status,])
#     #CSV Data
#     writer.writerows(output)
#     response['Content-Disposition'] = 'attachment; filename="voters.csv"'

#     return response

def export_voters_data(request):
    # query_set = "Datasheet.objects.all()"
    p = "SELECT * FROM datasheet JOIN temp_voter ON datasheet.email = temp_voter.email WHERE temp_voter.email_confirmed=True OR temp_voter.verification_pending=True"
    cursor = connection.cursor()
    cursor.execute(p)
    query_set = cursor.fetchall()
    # print(query_set)
    output = []
    response = HttpResponse (content_type='text/csv')
    writer = csv.writer(response)
    #Header
    writer.writerow(['Name', 'Email', 'IP Address', 'Group', 'Round','Game', 'Voted For', 'Status'])
    for user in query_set:
        if user[15]:
            status = 'Valid'
        elif user[14]:
            status = 'Invalid'
        elif user[16]:
            status = 'Pending'
        else:
            status = 'Not Available'
        output.append([user[1], user[2], user[3], user[4], user[5], user[6], user[7], status,])
    #CSV Data
    writer.writerows(output)
    response['Content-Disposition'] = 'attachment; filename="voters.csv"'

    return response

def ip_address_list(request):
    # ip_list = list(Datasheet.objects.values("ip_address").order_by('the_count').annotate(the_count=Count('ip_address')))
    ip_list = Datasheet.objects.values('ip_address').annotate(Count('ip_address')).order_by('ip_address__count').filter(ip_address__count__gt=4)
    return render(request, 'upstaged_data/ip_address_list.html', context={'object_list': ip_list})

# Data Sheet Copy - linting
class DataSheetListView(ListView):
    model = Datasheet
    paginate_by = 10
    queryset = Datasheet.objects.all().order_by('name')

def link_voter_datasheet(request):
    vorter_list = Voter.objects.all()
    if vorter_list is not None:
        for v in vorter_list:
            votes_list = Datasheet.objects.filter(email=v.email)
            for vl in  votes_list:
                vl.voter_id = v
                vl.save()
    else:
        print(votes_list)
    
    # return redirect('upstaged_data:link-voter-datasheet')

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
            # v = Voter(name=uobj.name, email=uobj.email)
            # v.save()
            new_entry = new_entry +1
        else:
            skip_count = skip_count +1
            
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



def send_bulk_email_confirmation(request):
    new_voter_list = Voter.objects.filter(verification_pending=True, is_email_sent=False)[:30]
    for obj in new_voter_list:
        try:
            result = send_email_confirmation_link(request, obj ,obj.email)
        except Exception as e:
            print(e)
            pass  
    return redirect('upstaged_data:verification-emails-list')  

    
def send_email_confirmation(request, pk):
    obj = Voter.objects.get(pk=pk)
    result = send_email_confirmation_link(request, obj, obj.email)
    if result:
        return redirect('upstaged_data:verification-emails-list')
    
    return redirect('upstaged_data:verification-emails-list')
