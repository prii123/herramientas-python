import datetime
import os

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect
from openpyxl import load_workbook
from django.http import QueryDict
from django.views.generic import TemplateView



# Create your views here.
from .forms import ExcelFormConciliacion
from .conciliaciones_package import util
from .conciliaciones_package.ConciliacionBancaria import ConciliacionBancaria


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
            #try:
                archivo_bancos = request.FILES["archivo_bancos"]
                archivo_contable = request.FILES["archivo_contable"]
                querydict = QueryDict(request.POST.urlencode())
                token = querydict.get('csrfmiddlewaretoken')

                if archivo_contable.name == archivo_bancos.name:
                    mensaje = "Los archivos cargados no pueden tener el mismo nombre"
                    return render(request, 'error.html', {'mensaje': mensaje})

                if util.verificar_columnas(archivo_bancos) and util.verificar_columnas(archivo_contable):
                    carpeta_destino = os.getcwd().split('buscador')[0] + '/archivos/'
                    dest_bancos = util.copiar_archivo(archivo_bancos, carpeta_destino, token)
                    dest_contable = util.copiar_archivo(archivo_contable, carpeta_destino, token)
                    querydict = QueryDict(request.POST.urlencode()).copy()
                    querydict['bancos'] = dest_bancos
                    querydict['contable'] = dest_contable
                    url_completa = f'/conciliaciones_preparacion?{querydict.urlencode()}'

                    return HttpResponseRedirect(url_completa)  # Redirección a la URL completaargs para pasar los pa
                    #return HttpResponseRedirect('/conciliaciones_preparacion')
                else:
                    mensaje = "Uno de los dos Archivos no contiene las columnas necesarias"
                    context= {'mensaje': mensaje}
                    return render(request, 'error.html', context)

            #except:
            #    return render(request, 'error.html')

    else:
        form = ExcelFormConciliacion()
        return render(request, 'conciliaciones.html', {'form': form})

def vista_conciliaciones_preparacion(request):
    dest_bancos = request.GET.get('bancos')
    dest_contable = request.GET.get('contable')

    if request.method == 'POST':
        # Obtener el valor del radio button
        opcion_seleccionada = request.POST.get('opcion')
        dest_bancos = dest_bancos.split(".xlsx")[0]
        dest_contable = dest_contable.split(".xlsx")[0]

        token = dest_contable.split(".")[0]
        nombre = token+".conciliacion"

        if int(opcion_seleccionada) == 1:
            concilia = ConciliacionBancaria(
                pathArchivoExtracto=dest_bancos, pathArchivoContable=dest_contable,
                nombreArchivoGenerado=nombre)
            concilia.definir_id()
            concilia.modular_duplicados()
            concilia.conciliacion_bancaria()
            concilia.generar_conciliacion()

        context={"nombre_archivo": nombre+".xlsx"}

        return render(request, 'downLoadFileConciliacion.html', context)

    else:

        subcadenas = dest_bancos.split(".xlsx")
        print(subcadenas)

        return render(request, 'conciliaciones_preparacion.html', {
            'bancos': dest_bancos,
            'contable': dest_contable,
        })
        #return render(request, 'conciliaciones_preparacion.html')

def descargar_archivo(request):
    param = request.GET.get('parametro')
    nom1 = param.split("archivos\\")[1]
    nom2 = nom1.split(".")[0]
    print('nom1')
    #print(nom2)

    #file_path = os.path.join(os.getcwd().split('buscador')[0] + '\\archivos\\'+param)

    if os.path.exists(param):
        with open(param, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(param))

            # Eliminar el archivo después de descargarlo
            #f.close()
            #os.remove(param)
            #borrar_archivos()
            borrar_archivos(nom2)
            return response
    else:
        return HttpResponse("El archivo no existe.")

def borrar_archivos(cadena):
    #print(cadena,"-------")
    ruta = os.getcwd().split('buscador')[0] + '\\archivos\\'
    archivos = os.listdir(ruta)
    print(archivos)
    for archivo in archivos: #os.listdir('.'):
        info_archivo = os.stat(archivo)
        #fecha_creacion = info_archivo.st_ctime
        print(archivo, info_archivo)
        #print(archivo)
        #if cadena in archivo:
            #os.remove(archivo)
            #print("")


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
