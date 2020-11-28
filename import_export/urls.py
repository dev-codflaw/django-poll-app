from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from import_export.views import (
    EmailUpload, 
    EmailDumpList, 
    send_email_confirmation, 
    VerifiedEmailList, 
    DateWiseEmailList, 
    DataSheetUpload, 
    PendingEmailList,
    InvalidEmailList,
    DataSheetListView,
    load_unique_emails,
    IsEmailSendList,
    # IPAddressList,
    ip_address_list,
)


app_name = 'import_export'

urlpatterns = [

    path('data-sheet/upload/', DataSheetUpload.as_view(), name="data-sheet-upload"),

    path('data-sheet/email/load/', load_unique_emails, name="email-load"),

    path('email/voter/', EmailDumpList.as_view(), name='unique-emails'),
    path('email/voter/verified/', VerifiedEmailList.as_view(), name='all-verified-emails'),
    path('email/voter/pending/', PendingEmailList.as_view(), name='all-pending-emails'),
    path('email/voter/invalid/', InvalidEmailList.as_view(), name='all-invalid-emails'),
    path('email/voter/verification/email/', IsEmailSendList.as_view(), name='verification-emails-list'),

    # path('email/voter/ip-address/', IPAddressList.as_view(), name='ip-address-list'),

    path('email/voter/ip-address/', ip_address_list, name='ip-address-list'),

    path('data-sheet/', DataSheetListView.as_view(), name='data-sheet'),

    path('email/user/date/', DateWiseEmailList.as_view(), name='date-wise-emails'),
    path('send-email-confirmation-link/<int:pk>/', send_email_confirmation, name='send_email_cnfrm'),


]