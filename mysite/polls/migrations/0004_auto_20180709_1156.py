# Generated by Django 2.0.7 on 2018-07-09 09:56

from django.db import migrations
import django_db_constraints.operations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_auto_20180709_1155'),
    ]

    operations = [
        django_db_constraints.operations.AlterConstraints(
            name='infrasctructure',
            db_constraints={'no_range': 'check (no >=1 AND no <=24 )', 'value_range': 'check (value >=0.0 AND value <=1.0 )'},
        ),
    ]
