# Generated by Django 2.2 on 2020-11-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSheetFromCommonNinja',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('ip_address', models.TextField()),
                ('group', models.CharField(max_length=50)),
                ('round', models.TextField()),
                ('game', models.CharField(max_length=5)),
                ('voted_for', models.CharField(max_length=50)),
                ('vote_timestamp', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Email_Dump',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.TextField()),
                ('invalid', models.BooleanField(default=False)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('varification_pending', models.BooleanField(default=False)),
                ('vote_time', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('address', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=150, unique=True)),
                ('profile', models.TextField()),
            ],
        ),
    ]
