# Generated by Django 2.0.7 on 2018-07-09 11:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0011_auto_20180709_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=12, validators=[django.core.validators.RegexValidator(regex='^[\\-a-zA-Z0-9]*$')])),
                ('max_human_silhouettes_no', models.PositiveIntegerField()),
                ('origin_camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Camera')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='camera_goal',
            unique_together={('camera', 'goal')},
        ),
    ]
