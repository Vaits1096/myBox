from django.urls import path
from . import views
from .views import ExercisesPageView

urlpatterns = [
    path('', views.index, name='index'),
    path('ejemplo/', views.ejemplo, name='ejemplo'),
    path('exercises/', ExercisesPageView.as_view(), name='exercises'),
    path('createexercises/', views.CreateExercise, name='add exercide'),
]
