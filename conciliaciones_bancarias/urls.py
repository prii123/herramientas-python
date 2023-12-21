from django.urls import path
from . import views
from .views import MenuView

urlpatterns = [
    path('x', views.vista, name='home'),
    path('conciliaciones', views.vista_conciliaciones, name='conciliaciones'),
    path('', MenuView.as_view(), name="menu")

]