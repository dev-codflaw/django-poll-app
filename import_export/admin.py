from django.contrib import admin

# Register your models here.

from import_export.models import Email_Dump, DataSheetFromCommonNinja


def make_pending(modeladmin, request, queryset):
    queryset.update(varification_pending=True)
make_pending.short_description = "Mark selected email as pending"

def make_invalid(modeladmin, request, queryset):
    queryset.update(invalid=True)
make_invalid.short_description = "Mark selected email as invalid"

def make_confirm(modeladmin, request, queryset):
    queryset.update(varification_pending=True, email_confirmed=True)
make_confirm.short_description = "Mark selected email as confirmed"

@admin.register(Email_Dump)
class VoterAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "email_confirmed", "varification_pending", "invalid")
    search_fields = ('name', 'email', )
    actions = [make_pending, make_confirm, make_invalid]


@admin.register(DataSheetFromCommonNinja)
class DastasheetAdmin(admin.ModelAdmin):
    search_fields = ('name', 'email', )
    list_display = ("id", "name", "email", "updated_at")
