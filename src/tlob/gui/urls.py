from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('listFunctions/', views.listFunctions, name='listFunctions'),
    path('addModule/', views.addModule, name='addModule'),
    path('confirmModule/', views.confirmModule, name='confirmModule'),
    path('confirmDesign/', views.confirmDesign, name='confirmDesign'),
    path('confirmConnection/', views.confirmConnection, name='confirmConnection'),
    path('confirmBus/', views.confirmBus, name='confirmBus'),
]