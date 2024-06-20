from rest_framework import serializers
from .models import CustomUser,Crop,CropSensorData,CropSchedule


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = '__all__'

class CropSensorDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSensorData
        fields = '__all__'

class CropScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropSchedule
        fields = '__all__'