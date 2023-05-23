from django.urls import path

from . import views

urlpatterns = [
    path('', views.vista),
    path('buscador/', views.buscar_dian),
    path('descargar-archivo/', views.descargar_archivo),
]