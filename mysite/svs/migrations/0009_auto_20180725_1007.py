# Generated by Django 2.1b1 on 2018-07-25 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('svs', '0008_auto_20180725_1004'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Component',
        ),
        migrations.AlterField(
            model_name='svs_output',
            name='svs_id',
            field=models.IntegerField(unique=True),
        ),
    ]
