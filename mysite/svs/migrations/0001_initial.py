# Generated by Django 2.1b1 on 2018-07-25 06:33

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_db_constraints.operations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('period', models.IntegerField(blank=True, null=True)),
                ('unit', models.CharField(blank=True, default='ms', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=100)),
                ('expression', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=12)),
                ('priority', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Camera',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.SlugField(max_length=12)),
                ('ip', models.GenericIPAddressField(default='0.0.0.0', protocol='IPv4')),
                ('login', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Camera_type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_model', models.CharField(max_length=100)),
                ('custom_camera_url', models.CharField(help_text='Use {admin} and {password} for creditentials, and {ip} for adress of the webcam', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Component_action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='svs.Action')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='svs.Component')),
            ],
        ),
        migrations.CreateModel(
            name='Infrasctructure',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=2)),
                ('no', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)])),
                ('value', models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1.0)])),
                ('max', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('min', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recognition_goal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('type', models.CharField(max_length=50)),
                ('complexity', models.CharField(max_length=10)),
                ('agregator', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.SlugField(max_length=12)),
                ('max_human_silhouettes_no', models.PositiveIntegerField(blank=True, null=True)),
                ('origin_camera', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='svs.Camera')),
            ],
        ),
        migrations.CreateModel(
            name='Zone_polygon',
            fields=[
                ('point_no', models.AutoField(primary_key=True, serialize=False)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='polygons', to='svs.Zone')),
            ],
        ),
        migrations.AddField(
            model_name='recognition_goal',
            name='zone',
            field=models.ManyToManyField(related_name='goals', to='svs.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='infrasctructure',
            unique_together={('type', 'no')},
        ),
        migrations.AddField(
            model_name='camera',
            name='camera_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camera_types', to='svs.Camera_type'),
        ),
        migrations.AddField(
            model_name='alert',
            name='component_action',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='svs.Component_action'),
        ),
        migrations.AddField(
            model_name='alert',
            name='zone',
            field=models.ManyToManyField(to='svs.Zone'),
        ),
        migrations.AlterUniqueTogether(
            name='zone_polygon',
            unique_together={('x', 'y', 'zone')},
        ),
        migrations.AlterUniqueTogether(
            name='zone',
            unique_together={('name', 'origin_camera')},
        ),
        django_db_constraints.operations.AlterConstraints(
            name='Infrasctructure',
            db_constraints={'no_range': 'check (no >=1 AND no <=24 )', 'value_range': 'check (value >=0.0 AND value <=1.0 )'},
        ),
        django_db_constraints.operations.AlterConstraints(
            name='Zone_polygon',
            db_constraints={'point_values': 'check (point_no >=1)'},
        ),
    ]
