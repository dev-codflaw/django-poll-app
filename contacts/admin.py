from django.contrib import admin

# Register your models here.
from contacts.models import Contacts, Label


admin.site.register(Contacts)
admin.site.register(Label)