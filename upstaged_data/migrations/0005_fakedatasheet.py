# Generated by Django 2.2 on 2020-12-02 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upstaged_data', '0004_remove_datasheet_voter_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='FakeDatasheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('ip_address', models.CharField(max_length=20)),
                ('group', models.CharField(max_length=50)),
                ('round', models.CharField(max_length=50)),
                ('game', models.CharField(max_length=5)),
                ('voted_for', models.CharField(max_length=150)),
                ('vote_time', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'fake_datasheet',
                'ordering': ['name'],
            },
        ),
    ]