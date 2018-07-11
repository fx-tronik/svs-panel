from django.contrib import admin
from django import forms


from .models import Infrasctructure, Camera, Recognition_goal, Zone, Zone_alert
from .models import Zone_polygon, Zone_goal, Component, Action, Component_action, Alert, Test

class Zone_polygon_inline(admin.TabularInline):
    model = Zone_polygon
    extra = 0

class Zone_goal_inline(admin.TabularInline):
    model = Zone_goal
    extra = 0

class ZoneAdmin(admin.ModelAdmin):
    inlines = [Zone_polygon_inline, Zone_goal_inline]


admin.site.register(Infrasctructure)
admin.site.register(Camera)
admin.site.register(Recognition_goal)
admin.site.register(Zone, ZoneAdmin)
admin.site.register(Zone_alert)
admin.site.register(Component)
admin.site.register(Action)
admin.site.register(Component_action)
admin.site.register(Alert)
admin.site.register(Test)
