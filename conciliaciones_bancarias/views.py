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
from .forms import ExcelFormConciliacion

def vista(request):
    if request.method == 'POST':
        form = ExcelFormConciliacion(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = request.FILES['test']
            workbook = load_workbook(archivo_excel)
            # Obtiene la primera hoja del libro de trabajo
            sheet = workbook.active

            print(sheet)

            querydict = QueryDict(request.POST.urlencode())
            valor = querydict.get('csrfmiddlewaretoken')

            print(valor)
            context = {
                'archivo': 'archivo',
                'exito': True,
                'nombre_archivo': 'nombre_retornado'
            }

            return render(request, 'downLoadFileConciliacion.html')

    else:
        form = ExcelFormConciliacion()
        return render(request, 'conciliaciones.html', {'form': form})

def vista_conciliaciones(request):
    if request.method == 'POST':
        form = ExcelFormConciliacion(request.POST, request.FILES)
        if form.is_valid():
            try:
                archivo_bancos = request.FILES["archivo_bancos"]
                archivo_contable = request.FILES["archivo_contable"]
                print(archivo_bancos)
                print(archivo_contable)
                #workbook = load_workbook(archivo_excel)

                #sheet = workbook.active
                #print("tesssst")
                return render(request, 'downLoadFileConciliacion.html')
                # return redirect('herramientas', context=context)
            except:
                print("error --")
                return render(request, 'error.html')

    else:
        form = ExcelFormConciliacion()
        return render(request, 'conciliaciones.html', {'form': form})




def vista_home(request):
    return render(request, 'inicio.html')

def downLoadFileConciliacion(request):
    return render(request, 'downLoadFileConciliacion.html')




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