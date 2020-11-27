from django.db import models
# Create your models here.


# from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    address = models.CharField(max_length=50)
    phone = models.CharField(max_length=150,unique=True)
    profile = models.TextField()

    def __str__(self):
        return self.name



class Email_Dump(models.Model):
    name = models.CharField(max_length=50)
    email = models.TextField(unique=True)
    invalid = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    varification_pending = models.BooleanField(default=False)
    vote_time = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

    



class DataSheetFromCommonNinja(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    ip_address = models.TextField()
    group = models.CharField(max_length=50)
    round = models.CharField(max_length=50)
    game = models.CharField(max_length=5)
    voted_for = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

        