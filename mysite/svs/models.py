from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Infrasctructure(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)

    type = models.CharField(max_length=2)
    no = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    value = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1.0)], null=True, blank=True)
    max = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    min = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
            return self.type + ' ' + str(self.no)

    class Meta:
        unique_together = (("type", "no"),)
        db_constraints = {
            'value_range': 'check (value >=0.0 AND value <=1.0 )',
            'no_range': 'check (no >=1 AND no <=24 )',
        }


class Camera(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)

    name = models.SlugField(max_length=12)
    ip = models.GenericIPAddressField(protocol='IPv4', default='0.0.0.0')
    login = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    camera_type = models.ForeignKey('Camera_type', related_name='camera_types', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


# TODO We probably shouldnt create default zones for cameras that already have
# zones, this might happen when camera is created from zone creation form -
# origin_camera field
@receiver(post_save, sender=Camera)
def Camera_added(sender, instance, created, **kwargs):
    if created:
        Zone.objects.create(origin_camera=instance, name="default")


class Camera_type(models.Model):

    camera_model = models.CharField(max_length=100)
    custom_camera_url = models.CharField(max_length=50, blank=False, null=False,help_text="Use {admin} and {password} for creditentials, and {ip} for adress of the webcam")

    def __str__(self):
        return self.camera_model


class Zone(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True, )

    name = models.SlugField(max_length=12)
    max_human_silhouettes_no = models.PositiveIntegerField(null=True, blank=True)
    origin_camera = models.ForeignKey('Camera', related_name='zones', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.origin_camera) + ' - ' + self.name

    class Meta:
        unique_together = (("name", "origin_camera"),)


class Recognition_goal(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)

    zone = models.ManyToManyField(Zone, related_name='goals')
    type = models.CharField(max_length=50)
    complexity = models.CharField(max_length=10)
    agregator = models.CharField(max_length=50)

    def __str__(self):
        return self.type


class Zone_polygon(models.Model):

    point_no = models.AutoField(primary_key=True)

    zone = models.ForeignKey('Zone', related_name='polygons', on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()

    class Meta:
        unique_together = (("zone", "point_no"),)
        unique_together = (('x', 'y', 'zone'))
        db_constraints = {
            'point_values': 'check (point_no >=1)',
        }

    def __str__(self):
        return str(self.zone) + ' | ' + str(self.point_no)


# W moim zrozumieniu są to elementy którymi może sterować SVS - wolne wyjścia
# niewykorzystane przez wsad
#class Component(models.Model):

#    id = models.AutoField(primary_key=True, null=False, unique=True)

#    name = models.CharField(max_length=20)

#    def __str__(self):
#        return str(self.name)


class SVS_task(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)
    description = models.CharField(max_length=20, null=True)
    svs_task = models.CharField(max_length=20)

    def __str__(self):
        return self.description

class SVS_output(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)
    description = models.CharField(max_length=20, null=True)
    svs_id = models.IntegerField(unique=True)

    def __str__(self):
        return self.description


class Action(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)

    #svs_output = models.ManyToManyField(SVS_output)
    name = models.CharField(max_length=20)
    svs_output = models.ForeignKey('SVS_output', related_name='output', on_delete=models.PROTECT, null=True)
    svs_task = models.ForeignKey('SVS_task', related_name='task', on_delete=models.PROTECT, null=True)
    period = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True, default='ms')

    def __str__(self):
        return self.name

class Alert(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)

    zone = models.ManyToManyField(Zone)
    description = models.CharField(max_length=100)
    expression = models.CharField(max_length=50)
    type = models.CharField(max_length=12)
    priority = models.CharField(max_length=10)
    component_action = models.ManyToManyField('Action')

    def __str__(self):
        return self.description
