from django.urls import path
from . import views

urlpatterns = [
    path('animals/', views.AnimalsView.as_view()),
    path('animals/<int:animal_id>/', views.AnimalView.as_view())
]