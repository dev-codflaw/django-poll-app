# Generated by Django 2.2 on 2020-11-24 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('import_export', '0008_auto_20201124_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datasheetfromcommonninja',
            name='date',
            field=models.DateTimeField(),
        ),
    ]