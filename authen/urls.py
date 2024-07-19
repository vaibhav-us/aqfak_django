from django.urls import path
from . import views

urlpatterns = [
    path('sign/',views.signin),
   path('signup/',views.signup),
    path('signout/',views.signout),
    path('retreive_update_user/',views.retrieve_update_user),
    path('list_create_crop/',views.list_create_crop),
    path('getcrop_details/',views.getcrop_details),
    path('retreive_update_delete_crop/<str:id>/',views.retreive_update_delete_crop),
]
