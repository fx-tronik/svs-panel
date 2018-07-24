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

    class Meta:
        unique_together = (("name", "origin_camera"),)

    def __str__(self):
        return str(self.origin_camera) + ' - ' + self.name

class Recognition_goal(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)

    zone = models.ManyToManyField(Zone, related_name='goals')
    type = models.CharField(max_length=50)
    complexity = models.CharField(max_length=10)
    agregator = models.CharField(max_length=50)

    def __str__(self):
        return self.type

class Zone_polygon(models.Model):

    zone = models.ForeignKey('Zone', related_name='polygons', on_delete=models.CASCADE)
    point_no = models.AutoField(primary_key=True)
    #point_no = models.PositiveIntegerField(validators=[MinValueValidator(1)])
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


class Component(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class Action(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)
    name = models.CharField(max_length=20)
    period = models.IntegerField(null=True, blank=True)
    unit = models.CharField(max_length=20, null=True, blank=True, default='ms')

    def __str__(self):
        return self.name


class Component_action(models.Model):
    component = models.ForeignKey('Component', on_delete=models.CASCADE)
    action = models.ForeignKey('Action', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.component) + ' | ' + str(self.action)


class Alert(models.Model):

    id = models.AutoField(primary_key=True, null=False, unique=True)
    zone = models.ManyToManyField(Zone)
    description = models.CharField(max_length=100)
    excpression = models.CharField(max_length=50)
    type = models.CharField(max_length=12)
    priority = models.CharField(max_length=10)
    component_action = models.ForeignKey(
        'Component_action', on_delete=models.CASCADE)

    def __str__(self):
        return self.description
