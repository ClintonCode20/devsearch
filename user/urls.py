from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfile, name = 'profile'),
    path('profile/<str:pk>', views.ProfileDetail, name = 'profile-detail'),
    path('signup/', views.SignUp, name = 'signup'),
    path('signin/', views.SignIn, name = 'signin'),
    path('signout/', views.SignOut, name = 'signout'),
    path('user/account', views.UserAccount, name = 'account'),
    path('update-profile', views.UpdateProfile, name = 'update-profile'),
    path('create-skill', views.CreateSKill, name = 'create-skill'),
    path('update-skill/<str:pk>', views.UpdateSKill, name = 'update-skill'),
    path('delete-skill/<str:pk>', views.DeleteSkill, name = 'delete-skill'),
    path('inbox', views.SentMessages, name = 'inbox'),
    path('message/<str:pk>', views.ReadMessage, name = 'message'),
    path('send-message/<str:pk>', views.MessageProfile, name = 'send-message')
]
