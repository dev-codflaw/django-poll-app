# Generated by Django 2.2 on 2020-11-27 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='participant1',
        ),
        migrations.RemoveField(
            model_name='game',
            name='participant2',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='tournament',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='choice',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='question',
        ),
        migrations.RemoveField(
            model_name='vote',
            name='user',
        ),
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
        migrations.DeleteModel(
            name='Tournament',
        ),
        migrations.DeleteModel(
            name='Vote',
        ),
    ]