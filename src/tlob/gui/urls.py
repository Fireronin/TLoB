from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listFunctions/', views.listFunctions, name='listFunctions'),
    path('addModule/', views.addModule, name='addModule'),
]