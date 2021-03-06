# Generated by Django 2.0.7 on 2018-07-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_camera'),
    ]

    operations = [
        migrations.AddField(
            model_name='camera',
            name='ip',
            field=models.GenericIPAddressField(default='0.0.0.0', protocol='IPv4'),
        ),
        migrations.AddField(
            model_name='camera',
            name='login',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='camera',
            name='password',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
