import os

from django.http import HttpResponse
from django.http import QueryDict
from django.shortcuts import render
from openpyxl import load_workbook

from .buscadorDIAN import buscadorDIAN
from .forms import ExcelForm
from .models import Cliente


# Create your views here.


def vista(request):
    if request.method == 'POST':
        form = ExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = request.FILES['archivo_excel']
            workbook = load_workbook(archivo_excel)
            # Obtiene la primera hoja del libro de trabajo
            sheet = workbook.active

            # Obtiene los valores de la primera columna en una listaa
            primera_columna = []
            for row in sheet.iter_rows(values_only=True):
                primera_columna.append(row[0])

            querydict = QueryDict(request.POST.urlencode())
            valor = querydict.get('csrfmiddlewaretoken')

            # print(primera_columna)
            # buscar_dian(primera_columna,valor)

            buscador = buscadorDIAN("nit", valor)
            cliente = Cliente
            datos_encontrados = []
            for nit in primera_columna:

                cli = cliente.obtener_cliente_por_nit(nit)
                if cli:
                    fila = [cli.nit, cli.apellido1, cli.apellido2, cli.nombre1, cli.nombre2, cli.razon_social,
                            cli.estado]
                    datos_encontrados.append(fila)
                    print(cli.nit, cli.apellido1, cli.apellido2, cli.nombre1, cli.nombre2, cli.razon_social, cli.estado,
                          "en base de datos")

                else:
                    dato = buscador.unaBusqueda(nit)
                    datos_encontrados.append(dato)
                    print(dato, "en buscador dian")
                    # buscador.multiples_busquedas()

            nombre_retornado = buscador.archivo_excel(datos_encontrados)

            context = {
                'archivo': 'archivo',
                'exito': True,
                'nombre_archivo': nombre_retornado
            }

            return render(request, 'resultado.html', context)


    else:
        form = ExcelForm()
        return render(request, 'buscador.html', {'form': form})


def descargar_archivo(request):
    param = request.GET.get('parametro')
    # print(param)
    file_path = os.path.join(os.getcwd().split('buscador')[0] + '\\archivos\\' + param)

    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(os.path.basename(file_path))
            return response
    else:
        return HttpResponse("El archivo no existe.")


def buscar_dian(data, nombre_archivo):
    buscador = buscadorDIAN(data, nombre_archivo)
    buscador.multiples_busquedas()
    buscador.archivo_excel()
