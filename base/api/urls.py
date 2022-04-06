from unicodedata import name
from django.urls import path
from .views import RegisterView,VerifyEmail, RegisterUserNor,RegisterUserBo
from . import views 
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('',views.getRoutes),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email-verify/',VerifyEmail.as_view(),name='email-verify'),
    path('imageUpload/',views.imageUpload, name='uploadInage'),
    path('allImage/<str:pk>',views.allImage),
    path('allUploadedImage/',views.allUploadedImage),
    path('imageStatusChange/',views.imageStatusChange),
    path('saveComment/',views.saveComment),
    path('saveContractInfo/',views.saveContractInfo),
    path('indivudualAllImages/<str:pk>',views.indivudualAllImages),
    path('setEventInfo/',views.setEventInfo),
    path('orderPrice/',views.orderPrice),
    path('saveContract/',views.saveContract), 
    path('getContract/',views.getContract),
    path('getAllContract/',views.getAllContract),
    path('upPinataImg/',views.upPinataImg),
    path('getClickUp/',views.getClickUp),
    path('saveCID/',views.saveCID),
    path('getCID/',views.getCID),
    path('saveJsonCID/',views.saveJsonCID), 
    path('generateNFT/',views.generateNFT),
    path('getjsonCID/',views.getjsonCID),
    path('getSellOrderContract/',views.getSellOrderContract),
    path('saveOrderPrice/',views.saveOrderPrice),


    #############################################

    path('registerBoUser/', RegisterUserBo.as_view(), name='user_save'),
    path('registerNorUser/', RegisterUserNor.as_view(), name='user_save'),
    path('getRole/', views.getRoles, name='roles'),
    path('setUserRole/', views.setUserRole, name='userRoles'),
    path('boUser/', views.getBoUser, name='boUser'),
    path('singleUserRole/<str:email>', views.getSingleUserRole, name='singleUserRole'),
 

    ##################################

    path('action-get/', views.GetSingleOrAllAction),
    path('action-get/<str:action_name>/', views.GetSingleOrAllAction),
    path('rolewiseaction-save/', views.RoleActionSave),
    path('rolewiseaction-edit/',views.RoleActionEdit),
    path('rolewiseaction-get/', views.RoleWiseActionAllOrSingle),
    path('rolewiseaction-get/<str:id>', views.RoleWiseActionAllOrSingle),

    #############################################################
    path('allImage1/<str:pk>',views.allImage),

    path('imageUpload1/',views.imageUpload1, name='uploadInage'),

]