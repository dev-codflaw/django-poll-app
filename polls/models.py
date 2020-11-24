import datetime

from django.db import models
from django.utils import timezone
from accounts.models import User


class Tournament(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(blank=True)
    start_timestamp = models.DateTimeField(blank=True, null=True)
    end_timestamp = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(blank=True)
    email = models.EmailField(blank=True)
    website = models.CharField(max_length=50, blank=True)
    video_url = models.CharField(max_length=150, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Round(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Game(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    participant1 = models.ForeignKey(Participant, related_name='participant1', on_delete=models.DO_NOTHING,  null=True)
    participant2 = models.ForeignKey(Participant, related_name='participant2' ,on_delete=models.DO_NOTHING, null=True)
    location = models.CharField(max_length=50, blank=True)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    event_text = models.CharField(max_length=200, default='Default event text')
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    is_voted = models.IntegerField(default=0)