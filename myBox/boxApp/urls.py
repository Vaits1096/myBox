from django.urls import path
from . import views
from .views import ExercisesPageView
from accounts.views import welcome

app_name = 'boxApp'
urlpatterns = [
    path('', welcome, name='index'),
    path('ejemplo/', views.ejemplo, name='ejemplo'),
    path('exercises/', ExercisesPageView.as_view(), name='exercises'),
    path('createexercises/', views.CreateExercise, name='add_exercise'),
    path('create_athlete/', views.create_athlete, name='create_athlete'),
    path('create_user/', views.create_user, name='create_user'),
    path('activate_account/', views.activate_account, name='activate_account'),
]