from django.contrib import admin
from .models import CustomUser, Crop, CropSensorData, CropSchedule

admin.site.register(CustomUser)
admin.site.register(Crop)
admin.site.register(CropSensorData)
admin.site.register(CropSchedule)
