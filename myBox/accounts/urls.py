from django.contrib import admin
from django.urls import path
from accounts import views

app_name = 'accounts'
urlpatterns = [
    #path('', views.welcome),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]