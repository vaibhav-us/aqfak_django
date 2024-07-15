from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import CustomUser,Crop, CropSensorData, CropSchedule
from .serializers import CustomUserSerializer,CropSerializer,CropSensorDataSerializer,CropScheduleSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login,logout,authenticate
from .utility import capitalizeDict
from django.shortcuts import get_object_or_404



@api_view(['POST'])
def signup(request):
    try:
        user_info = request.data['userInfo']
        crops = request.data['crops']
        user = User.objects.create(username=user_info["userId"])
        user.save()
        login(request,user)
        customuser = CustomUser.objects.create(user= user ,email=user_info["userId"],name=user_info["name"], profilePhoto=user_info["photo"])
        customuser.save()
        for crop in crops:
            crop_record = Crop.objects.create(user=customuser,name=crop['crop'],stage=crop['stage'],area=crop['area'])
            crop_record.save()
        return Response("data created")
    except Exception as e:
        return Response({'detail': f'Something went wrong', 'exception': str(e)})
    

@api_view(['POST'])
def signin(request):
    user_id = request.data["user_id"]
    try:
        user = User.objects.get(username = user_id)
    except ObjectDoesNotExist:
        user = None
        return Response("false")
    if user:
        login(request,user)
        return Response("true")

@api_view(['GET'])
def signout(request):
    logout(request)
    return Response("logged out")


@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
def retrieve_update_user(request):
    try:
        custom_user=CustomUser.objects.get(user=request.user)
        if request.method == 'GET':
            user_serializer = CustomUserSerializer(custom_user)
            return Response({"user":user_serializer.data})
        
        elif request.method == 'PUT':
            user_serializer = CustomUserSerializer(data=request.data,partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response({'detail': user_serializer.errors})
            return Response({"user":user_serializer.data})
    except Exception as e:
        return Response({'detail': f'Something went wrong', 'exception': str(e)})



@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def getuser_crops(request):
    try:
        custom_user = CustomUser.objects.get(user=request.user)
    except CustomUser.DoesNotExist:
        return Response("Model Does Not Exists")
    
    if request.method == "GET":
        crops = Crop.objects.filter(user=custom_user)
        cropSerializer = CropSerializer(crops, many=True)
        cropData = []
        for crop in cropSerializer.data:
            cropInstance = Crop.objects.get(id=crop['id'])  # Get Crop instance by ID
            sensor_data_instance = CropSensorData.objects.filter(crop=cropInstance).first()
            if sensor_data_instance:
                condition = CropSensorDataSerializer(sensor_data_instance).data['condition']
            else:
                condition = None
            crop['condition'] = condition
            cropData.append(capitalizeDict(crop))
        return Response(cropData)
    
    elif request.method =="PUT":

        crop_id = request.data['id']
        try:
            crop = Crop.objects.get(id=crop_id)
        except Crop.DoesNotExist:
            return Response({"error": "crop not found."})
        data = {
            "crop":request.data['crop'],
            "area":request.data['area'],
            "stage":request.data['stage'],  
        }
        crop_serializer = CropSerializer(crop,data=data,partial=True)
        if crop_serializer.is_valid():
            crop_serializer.save()
            return Response(crop_serializer.data)
        else:
            return Response({'detail': crop_serializer.errors})
    
    elif request.method =="DELETE":
        crop_id = request.data['id']
        try:
            crop = Crop.objects.get(id=crop_id)
        except Crop.DoesNotExist:
            return Response({"error": "crop not found."})
        if crop:
            crop.delete()
            return Response('deleted')
        



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getcrop_details(request) :
    custom_user = CustomUser.objects.get(user=request.user)
    crop = request.GET.get('crop')

    #getting instances
    cropInstance = Crop.objects.get(user=custom_user,name=crop )
    sensorData = {}
    try:
        sensorDataInstance = CropSensorData.objects.get(crop=cropInstance)
        sensorData = CropSensorDataSerializer(sensorDataInstance, many=False).data
        sensorData['npk'] = [                  
            sensorData.pop('nitrogen'),
            sensorData.pop('phosphorous'),
            sensorData.pop('potassium'),
        ]
        sensorData['id'] = sensorData.pop('crop') #replacing the primary key of sensor data with its foreign key crop.As they are onetoone relation, it shouldnt be a problem    

    except CropSensorData.DoesNotExist:
        sensorData = {}
     
    
    #getting data from instances
    crop = CropSerializer(cropInstance, many=False).data
    scheduleInstances = CropSchedule.objects.filter(crop = cropInstance)
    schedule = CropScheduleSerializer(scheduleInstances, many=True).data if scheduleInstances else []

    #merging separte columns of nitrogen ,phosphorous and potassium together
       
    #putting everything together
    crop.update(sensorData)
    crop = capitalizeDict(crop)
    crop['schedule'] = capitalizeDict(schedule)

    return Response(crop)

















