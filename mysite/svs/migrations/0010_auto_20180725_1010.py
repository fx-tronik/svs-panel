# Generated by Django 2.1b1 on 2018-07-25 08:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('svs', '0009_auto_20180725_1007'),
    ]

    operations = [
        migrations.CreateModel(
            name='SVS_task',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('svs_task', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='action',
            name='svs_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='task', to='svs.SVS_task'),
        ),
    ]
