from django.urls import path,include
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [ 

    #API
    path('register/',register.as_view()),
    path('register_recipient/',registerRec.as_view()),
    path('user_login/',csrf_exempt(user_login),name='user_login'),
    path('Allusers/',UserListView.as_view()),
    path('Updateuser/<id>/', UserUpdateView.as_view()),
    path('getuserbyId/<int:user_id>/',GetuserbyId.as_view()),

    #Request
    path('CreateRequest/',RequestCreateView.as_view()),
    path('Requestbyuserid/<int:user_id>/',Requestbyuserid.as_view()),
    path('UpdateRequest/<id>/', RequestUpdateView.as_view()),
    path('Allrequest/',RequestListView.as_view()),  
   ]