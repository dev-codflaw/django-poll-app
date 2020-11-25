from django.contrib import admin

# Register your models here.

from import_export.models import Profile, Email_Dump, DataSheetFromCommonNinja

admin.site.register(Profile)
# admin.site.register(Email_Dump)
admin.site.register(DataSheetFromCommonNinja)


@admin.register(Email_Dump)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "email_confirmed")
