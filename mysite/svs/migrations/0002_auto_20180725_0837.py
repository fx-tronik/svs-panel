# Generated by Django 2.1b1 on 2018-07-25 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actions',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('available_action', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='actions',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='action', to='svs.Actions'),
        ),
    ]
