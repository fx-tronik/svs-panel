# Generated by Django 2.1b1 on 2018-07-20 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svs', '0018_auto_20180720_0824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera_type',
            name='custom_camera_url',
            field=models.CharField(help_text='Use {admin} and {password} for creditentials, and {ip} for adress of the webcam', max_length=50),
        ),
    ]
