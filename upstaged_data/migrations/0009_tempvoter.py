# Generated by Django 2.2 on 2020-12-04 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstaged_data', '0008_duplicatevotes'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempVoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50, unique=True)),
                ('invalid', models.BooleanField(default=False)),
                ('email_confirmed', models.BooleanField(default=False)),
                ('verification_pending', models.BooleanField(default=True)),
                ('is_email_sent', models.BooleanField(default=False)),
                ('email_sent', models.IntegerField(default=0)),
                ('email_verification_source', models.CharField(default='Not Yet', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'temp_voter',
                'ordering': ['id'],
            },
        ),
    ]
