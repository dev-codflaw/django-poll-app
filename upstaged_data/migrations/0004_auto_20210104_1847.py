# Generated by Django 2.2 on 2021-01-04 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('upstaged_data', '0003_auto_20210104_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vote',
            name='voter',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='upstaged_data.VoterReact'),
        ),
    ]
