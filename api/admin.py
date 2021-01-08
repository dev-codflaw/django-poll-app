from django.contrib import admin
from import_export.admin import ExportMixin, ImportExportModelAdmin

# Register your models here.
from upstaged_data.models import Vote, VoterReact


@admin.register(Vote)
class VoteAdmin(ImportExportModelAdmin):
    search_fields = ['email']
    list_display = ['email', 'voted_for', 'game']


@admin.register(VoterReact)
class VoterAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'email')
    list_display = ("name", "email", "is_valid", "source")