from django.contrib import admin

# Register your models here.

from .models import Profile, Email_Dump

admin.site.register(Profile)
admin.site.register(Email_Dump)