from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from upstaged_data.views import (
    EmailUpload, 
    VoterList, 
    send_email_confirmation, 
    VerifiedEmailList, 
    DateWiseEmailList, 
    DataSheetUpload, 
    PendingEmailList,
    InvalidEmailList,
    DataSheetListView,
    load_unique_emails,
    IsEmailSendList,
    IPAddressList,
    ip_address_list,
    link_voter_datasheet,
    send_bulk_email_confirmation,
    IPVoterList,
    export_voters_data,
    IPVoterAction,
    DuplicateDataSheetFind,
    DuplicateVoteList,
    export_dulicate_entry,
    TempIPAddressList,
    TempIPVoterAction,
    TempIPVoterList,
    make_invalid_action_for_ip_voters,
)


app_name = 'upstaged_data'

urlpatterns = [

    path('data-sheet/upload/', login_required(DataSheetUpload.as_view()), name="data-sheet-upload"),
    path('data-sheet/upload/duplicate/', login_required(DuplicateDataSheetFind.as_view()), name="find-duplicates"),

    path('data-sheet/email/load/', login_required(load_unique_emails), name="email-load"),
    path('data-sheet/email/bulk-send/', login_required(send_bulk_email_confirmation), name="send_bulk-email"),


    path('data-sheet/email/load/', login_required(link_voter_datasheet), name="link-voter-datasheet"),

    path('voter/duplicate/votes/', login_required(DuplicateVoteList.as_view()), name='duplicate-vote-list'),
    path('voter/duplicate/votes/export/', login_required(export_dulicate_entry), name='export-duplicate-vote-list'),

    path('voter/', login_required(VoterList.as_view()), name='unique-emails'),
    path('voter/verified/', login_required(VerifiedEmailList.as_view()), name='all-verified-emails'),
    path('voter/pending/', login_required(PendingEmailList.as_view()), name='all-pending-emails'),
    path('voter/invalid/', login_required(InvalidEmailList.as_view()), name='all-invalid-emails'),
    path('voter/verification/email/', login_required(IsEmailSendList.as_view()), name='verification-emails-list'),

    path('voter/ip-address/', login_required(IPAddressList.as_view()), name='ip-address-list'),
    path('voter/ip-address/voter/', login_required(IPVoterList.as_view()), name='ip-address-voters'),
    path('voter/ip-address/voter/action/', login_required(IPVoterAction.as_view()), name='ip-voters-action'),

    path('voter/ip-address/test/', login_required(TempIPAddressList.as_view()), name='temp-ip-address-list'),
    path('voter/ip-address/voter/test/', login_required(TempIPVoterList.as_view()), name='temp-ip-address-voters'),
    path('voter/ip-address/voter/action/test/', login_required(TempIPVoterAction.as_view()), name='temp-ip-voters-action'),
    path('voter/ip-address/voter/action/test/invalid/', login_required(make_invalid_action_for_ip_voters), name='make-invalid-ip-voter'),





    path('voter/export/', login_required(export_voters_data), name='export-voters'),

    # path('email/voter/ip-address/', ip_address_list, name='ip-address-list'),

    path('data-sheet/', login_required(DataSheetListView.as_view()), name='data-sheet'),

    path('email/user/date/', login_required(DateWiseEmailList.as_view()), name='date-wise-emails'),
    path('send-email-confirmation-link/<int:pk>/', login_required(send_email_confirmation), name='send_email_cnfrm'),



]

