import datetime
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from openpyxl import load_workbook
from django.http import QueryDict
from django.views.generic import TemplateView

# Create your views here.
def vista(request):
    """
    if request.method == 'POST':

            querydict = QueryDict(request.POST.urlencode())
            valor = querydict.get('csrfmiddlewaretoken')


            context = {
                'archivo': 'archivo',
                'exito': True,
                'nombre_archivo': 'nombre_retornado'
            }

            return render(request, 'resultado.html', context)

    else:
    """
    return render(request, 'herramientas.html')

def vista_conciliaciones(request):

    return render(request, 'conciliaciones.html')




class MenuView(TemplateView):
  template_name = "menu.html"
  pages = [
      {
          "url": "/home",
          "title": "Inicio",
      },
      {
          "url": "/conciliaciones",
          "title": "conciliaciones",
      }
  ]