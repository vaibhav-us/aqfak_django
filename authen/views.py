from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import CustomUser,Crop, CropSensorData, CropSchedule
from .serializers import CustomUserSerializer,CropSerializer,CropSensorDataSerializer,CropScheduleSerializer
from django.core.exceptions import ObjectDoesNotExist

from .utility import capitalizeDict

from rest_framework.authtoken.models import Token



@api_view(['POST'])
def signup(request):
    try:
        user_info = request.data['userInfo']
        
        user = User.objects.create(username=user_info["userId"])
        user.save()
        token,created = Token.objects.get_or_create(user=user)
        customuser = CustomUser.objects.create(user= user ,email=user_info["userId"],name=user_info["nickname"], profilePhoto=user_info["photo"],place=user_info["place"])
        customuser.save()
        custom_user_serializer = CustomUserSerializer(customuser)
        
        return Response({'data': custom_user_serializer.data, 'token': token.key })
    except Exception as e:
        return Response({'detail': f'Something went wrong', 'exception': str(e)})
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def list_create_crop(request):
    try:
        # user= User.objects.get(username='vus09003@gmail.com')
        custom_user = CustomUser.objects.get(user=request.user)
    except CustomUser.DoesNotExist:
        return Response("Model Does Not Exists")
    
    if request.method == "GET":
        crops = Crop.objects.filter(user=custom_user)
        cropSerializer = CropSerializer(crops, many=True)
        cropData = []
        for crop in cropSerializer.data:
            cropInstanceId = crop['id'] # Get Crop instance by ID
            crop_instance = Crop.objects.get(id=cropInstanceId)
            sensor_data_instance = CropSensorData.objects.filter(crop=crop_instance).first()
            if sensor_data_instance:
                condition = CropSensorDataSerializer(sensor_data_instance).data['condition']
            else:
                condition = None
            crop['condition'] = condition
            cropData.append(capitalizeDict(crop))
        return Response(cropData)
    
    elif request.method == 'POST':
        crops = request.data['crops']
        for crop in crops:
            crop_record = Crop.objects.create(user=custom_user,name=crop['crop'],stage=crop['stage'],area=crop['area'])
            crop_record.save()
            crop_serializer = CropSerializer(crop_record)
            return Response({"data":"crops created"})
    

@api_view(['POST'])
def signin(request):
    user_id = request.data.get("user_id")
    try:
        user = User.objects.get(username = user_id)
    except ObjectDoesNotExist:
        user = None
        return Response("false")
    if user:
        custom_user = CustomUser.objects.get(user=user)
        custom_user_serializer = CustomUserSerializer(custom_user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'msg':'true','data': custom_user_serializer.data, 'token': token.key })

@api_view(['GET'])
def signout(request):
    try:
        request.user.auth_token.delete()
        return Response({'detail':'Successfully logged out'})
    except Exception as e :
        return Response({'detail': f'Something went wrong'})


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def retrieve_update_user(request):
    try:
        # user= User.objects.get(username='vus09003@gmail.com')
        custom_user=CustomUser.objects.get(user=request.user)
        if request.method == 'GET':
            user_serializer = CustomUserSerializer(custom_user)
            return Response({"user":user_serializer.data})
        
        elif request.method == 'PUT':
            user_serializer = CustomUserSerializer(custom_user,data=request.data,partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
            else:
                return Response({'detail': user_serializer.errors})
            return Response({"user":user_serializer.data})
        elif request.method == 'DELETE':
            if custom_user:
                custom_user.delete()
                return Response('deleted')
                
    except Exception as e:
        return Response({'detail': f'Something went wrong', 'exception': str(e)})

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def retreive_update_delete_crop(request,id):
    try:
        # user= User.objects.get(username='vus09003@gmail.com')
        custom_user = CustomUser.objects.get(user=request.user)
    except CustomUser.DoesNotExist:
        return Response("Model Does Not Exists")
    try:
        crop = Crop.objects.get(id=id,user=custom_user)
    except Crop.DoesNotExist:
        return Response({"error": "crop not found."})
    
    if request.method == "GET":
        cropSerializer = CropSerializer(crop)
        return Response(cropSerializer.data)
    
    elif request.method =="PUT":
        data = {
            "name":request.data['name'],
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

















