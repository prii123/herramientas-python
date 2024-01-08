from django.urls import path
from . import views
from .views import MenuView

urlpatterns = [
    path('', views.vista_home, name='home'),
    path('conciliaciones', views.vista_conciliaciones, name='conciliaciones'),
    path('menu', views.vista_home, name="home"),
    path('downLoadFileConciliacion/', views.downLoadFileConciliacion, name='downLoadFileConciliacion'),
    path('descargar/', views.descargar_archivo, name='descargar'),
    path('conciliaciones_preparacion', views.vista_conciliaciones_preparacion, name='conciliaciones_preparacion'),


]