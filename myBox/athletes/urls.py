from django.urls import path
from . import views

app_name = 'athletes'
urlpatterns = [
    path('', views.athlete_list_view, name = 'athlete_list'),
    path('<int:id>/', views.athlete_detail_view, name = 'athlete_detail'),
    #path('<int:id>/update/', athlete_update_view, name = 'athlete_update'),
    #path('<int:id>/delete/', athlete_delete_view, name = 'athlete_delete'),
]