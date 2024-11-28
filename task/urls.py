from django.contrib import admin
from django.urls import path, include

from task import views

urlpatterns = [
    path('add/', views.add_task, name='add_task'),
]