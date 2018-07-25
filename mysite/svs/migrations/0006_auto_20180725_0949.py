# Generated by Django 2.1b1 on 2018-07-25 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svs', '0005_auto_20180725_0947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='action',
            name='component',
        ),
        migrations.RemoveField(
            model_name='action',
            name='svs_output',
        ),
        migrations.AddField(
            model_name='action',
            name='svs_output',
            field=models.ManyToManyField(to='svs.SVS_output'),
        ),
    ]
