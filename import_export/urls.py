from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from import_export.views import profile_upload, EmailUpload, EmailDumpList, send_email_confirmation, VarifiedEmailList, DateWiseEmailList


app_name = 'import_export'

urlpatterns = [
    path('upload-csv/', profile_upload, name="profile_upload"),
    path('emails-upload-csv/', EmailUpload.as_view(), name="emails_upload"),
    path('email/user/', EmailDumpList.as_view(), name='users_email'),
    path('email/user/varified/', VarifiedEmailList.as_view(), name='all-varified-emails'),
    path('email/user/date/', DateWiseEmailList.as_view(), name='date-wise-emails'),
    path('send-email-confirmation-link/<int:pk>/', send_email_confirmation, name='send_email_cnfrm'),


]