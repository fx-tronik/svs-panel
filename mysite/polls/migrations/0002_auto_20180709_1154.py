# Generated by Django 2.0.7 on 2018-07-09 09:54

from django.db import migrations
import django_db_constraints.operations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        django_db_constraints.operations.AlterConstraints(
            name='infrasctructure',
            db_constraints={'value_range': 'check (value >=0.0 )'},
        ),
    ]
