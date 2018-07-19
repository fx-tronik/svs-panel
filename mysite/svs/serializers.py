from rest_framework import serializers
from .models import Camera, Zone, Zone_polygon, Recognition_goal, Camera_type

class Polygons_serializer(serializers.ModelSerializer):

    class Meta:
        model = Zone_polygon
        fields = ('x', 'y')


class GoalsSerializer(serializers.ModelSerializer):

    type = serializers.CharField()
    complexity = serializers.CharField()

    class Meta:
        model = Recognition_goal
        fields = ('type', 'complexity')

class ZoneSerializer(serializers.ModelSerializer):

    polygons = Polygons_serializer(many=True, read_only=True)
    goals = GoalsSerializer(many=True, read_only=True)

    class Meta:
        model = Zone
        fields = ('name', 'goals', 'max_human_silhouettes_no', 'polygons')


class CameraSerializer(serializers.ModelSerializer):

    zones = ZoneSerializer(many=True, read_only=True)
    #custom_camera_url = serializers.URLField(source='camera_type.custom_camera_url')
    login = serializers.CharField()
    password = serializers.CharField()
    formatted_url = serializers.SerializerMethodField()

    class Meta:
        model = Camera
        fields = ('name', 'ip', 'login', 'password', 'zones', 'formatted_url')
        depth = 1

    def get_formatted_url(self, obj):
        if obj.login is not None and obj.password is not None:
            return obj.camera_type.custom_camera_url.format(admin=obj.login, password=obj.password)
        else:
            return obj.camera_type.custom_camera_url.replace("{admin}:{password}@", "")
