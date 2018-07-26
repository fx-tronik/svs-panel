from django.contrib import admin
# from django import forms
from .models import (
    Infrasctructure, Camera, Recognition_goal,
    Zone, Camera_type, Zone_polygon, #Component,
    Action, Alert, ARM_output, ARM_task
)


# class MyForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(MyForm, self).__init__(*args, **kwargs)
#         self.fields['custom_camera_url'].help_text = self.fields['custom_camera_url'].help_text.format(admin="blablabla", password="test")

class Zone_polygon_inline(admin.TabularInline):
    model = Zone_polygon
    extra = 0


class Recognition_goal_inline(admin.TabularInline):
    model = Recognition_goal.zone.through
    extra = 0


class ZoneAdmin(admin.ModelAdmin):
    inlines = [Zone_polygon_inline, Recognition_goal_inline]


class CameraAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Podstawowe dane', {'fields': ['name', 'ip', 'login', 'password']}),
        ('Typ kamery', {'fields': ['camera_type'],}),
    ]


class Camera_typeAdmin(admin.ModelAdmin):
#         form = MyForm
        fieldsets = [
            ('Podstawowe dane', {'fields': ['camera_model', 'custom_camera_url'],}),
        ]


admin.site.register(Infrasctructure)
admin.site.register(Camera, CameraAdmin)
admin.site.register(Recognition_goal)
admin.site.register(Zone, ZoneAdmin)
# admin.site.register(Zone_alert)
# admin.site.register(Component)
admin.site.register(Action)
admin.site.register(Alert)
admin.site.register(Camera_type, Camera_typeAdmin)
admin.site.register(ARM_output)
admin.site.register(ARM_task)
