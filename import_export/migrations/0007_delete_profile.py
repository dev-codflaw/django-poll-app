# Generated by Django 2.2 on 2020-11-27 20:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('import_export', '0006_remove_datasheetfromcommonninja_vote_timestamp'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]