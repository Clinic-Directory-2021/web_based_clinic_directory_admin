from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('request/', views.request, name='request'),
    path('clinic/', views.clinic, name='clinic'),
    path('settings/', views.settings, name='settings'),
    path('login_validation/', views.login_validation, name='login_validation'),
    path('logout/', views.logout, name='logout'),
    path('acceptClinic/', views.acceptClinic, name='acceptClinic'),
    path('declineClinic/', views.declineClinic, name='declineClinic'),
]