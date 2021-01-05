from django.db import models
# Create your models here.



class Voter(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    invalid = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    verification_pending = models.BooleanField(default=True)
    is_email_sent = models.BooleanField(default=False)
    email_sent = models.IntegerField(default=0)
    email_verification_source = models.CharField(max_length=100, default='Not Yet')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        db_table = 'voter'



class TempVoter(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,unique=True)
    invalid = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    verification_pending = models.BooleanField(default=True)
    is_email_sent = models.BooleanField(default=False)
    email_sent = models.IntegerField(default=0)
    email_verification_source = models.CharField(max_length=100, default='Not Yet')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        db_table = 'temp_voter'
        

class Datasheet(models.Model):
    # voter_id = models.ForeignKey(Voter, on_delete=models.DO_NOTHING, default=None, null=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20)
    group = models.CharField(max_length=50)
    round = models.CharField(max_length=50)
    game = models.CharField(max_length=5)
    voted_for = models.CharField(max_length=150)
    vote_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'datasheet'
        


class TempDatasheet(models.Model):
    # voter_id = models.ForeignKey(Voter, on_delete=models.DO_NOTHING, default=None, null=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20)
    group = models.CharField(max_length=50)
    round = models.CharField(max_length=50)
    game = models.CharField(max_length=5)
    voted_for = models.CharField(max_length=150)
    vote_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'temp_datasheet'



class DuplicateVotes(models.Model):
    # voter_id = models.ForeignKey(Voter, on_delete=models.DO_NOTHING, default=None, null=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    ip_address = models.CharField(max_length=20)
    group = models.CharField(max_length=50)
    round = models.CharField(max_length=50)
    game = models.CharField(max_length=5)
    voted_for = models.CharField(max_length=150)
    vote_time = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'duplicate_votes'



class VoterReact(models.Model):
    name = models.CharField(max_length=30)
    email =  models.CharField(max_length=50)
    is_valid = models.BooleanField(default=False)
    source = models.CharField(max_length=30, default='Not Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'voter_react'
        verbose_name = 'voter_react'
        verbose_name_plural = 'voter_reacts'

class Vote(models.Model):
    # voter = models.ForeignKey(VoterReact, on_delete=models.DO_NOTHING, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    game = models.CharField(max_length=30)
    voted_for = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'vote'
        verbose_name = 'vote'
        verbose_name_plural = 'votes'