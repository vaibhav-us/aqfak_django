from django.urls import path
from . import views

urlpatterns = [
    path('sign/',views.signin),
   path('signup/',views.signup),
    path('signout/',views.signout),
    path('getuser/',views.get_user_details),
    path('getuser_crops/',views.getuser_crops),
    path('getcrop_details/',views.getcrop_details),
]
