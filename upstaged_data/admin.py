from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin

# Register your models here.
from upstaged_data.models import Voter, Datasheet
# from upstaged_data.admin import ImportExportModelAdmin

def make_pending(modeladmin, request, queryset):
    queryset.update(verification_pending=True, email_confirmed=False, invalid=False, email_verification_source='by admin')
make_pending.short_description = "Mark selected email as pending"

def make_invalid(modeladmin, request, queryset):
    queryset.update(invalid=True, verification_pending=False, email_confirmed=False, email_verification_source='by admin')
make_invalid.short_description = "Mark selected email as invalid"

def make_confirm(modeladmin, request, queryset):
    queryset.update(verification_pending=False, email_confirmed=True, email_verification_source='by admin')
make_confirm.short_description = "Mark selected email as confirmed"

@admin.register(Voter)
class VoterAdmin(ImportExportModelAdmin):
    list_display = ("id", "name", "email", "email_confirmed", "verification_pending", "invalid", "is_email_sent", "email_sent", "email_verification_source")
    search_fields = ('name', 'email', )
    actions = [make_pending, make_confirm, make_invalid]


@admin.register(Datasheet)
class DatasheetAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'email', 'ip_address')
    list_display = ("id", "name", "email", "game","updated_at", "ip_address", "vote_time")

