# Generated by Django 2.2 on 2020-12-30 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0003_auto_20201230_1806'),
    ]

    operations = [
        migrations.RenameField(
            model_name='label',
            old_name='name',
            new_name='title',
        ),
        migrations.AddField(
            model_name='label',
            name='color',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='label',
            name='description',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='label',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
