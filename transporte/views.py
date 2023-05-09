from django.shortcuts import render, redirect
from .models import Transporte, Escuela
from .forms import TransporteForm
from django.db.models import Q, Sum
from .forms import EscuelaForm
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.http import FileResponse
from datetime import datetime
from django.template.loader import get_template
# from xhtml2pdf import pisa
from io import BytesIO


# @login_required
def transporte_list(request):
    query = request.GET.get('q', '')
    if query:
        transportes = Transporte.objects.filter(
            Q(patente__icontains=query) |
            Q(oferente__icontains=query) |
            Q(cantidad_km__icontains=query) |
            Q(alumnos__icontains=query) |
            Q(sectores__icontains=query) |
            Q(escuela__nombre__icontains=query)
        )
    else:
        transportes = Transporte.objects.all()
    total_km = transportes.aggregate(Sum('cantidad_km'))['cantidad_km__sum']
    total_alumnos = transportes.aggregate(Sum('alumnos'))['alumnos__sum']
    return render(request, 'transporte/transporte_list.html', {'transportes': transportes, 'total_km': total_km, 'total_alumnos': total_alumnos})


# @login_required
def transporte_create(request):
    if request.method == 'POST':
        form = TransporteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transporte_list')
    else:
        form = TransporteForm()
    return render(request, 'transporte/transporte_form.html', {'form': form})


# @login_required
def transporte_update(request, patente):
    transporte = Transporte.objects.get(patente=patente)
    if request.method == 'POST':
        form = TransporteForm(request.POST, instance=transporte)
        if form.is_valid():
            form.save()
            return redirect('transporte_list')
    else:
        form = TransporteForm(instance=transporte)
    return render(request, 'transporte/transporte_form.html', {'form': form})


# @login_required
def transporte_delete(request, patente):
    transporte = Transporte.objects.get(patente=patente)
    transporte.delete()
    return redirect('transporte_list')


# @login_required
def escuela_create(request):
    if request.method == 'POST':
        form = EscuelaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transporte_list')
    else:
        form = EscuelaForm()
    return render(request, 'transporte/escuela_form.html', {'form': form})


# @login_required
def profile_view(request):
    return render(request, 'transporte_list.html')

# aqui van las funciones de exportar a excel, csv y pdf


# def export_escuelas_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="escuelas.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['RBD', 'Digito Verificador', 'Nombre'])

#     data = Escuela.objects.all().values_list('rbd', 'digito_verificador', 'nombre')
#     for row in data:
#         writer.writerow(row)

#     return response


# def export_transportes_csv(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="transportes.csv"'

#     writer = csv.writer(response)
#     writer.writerow(['Patente', 'Oferente', 'Cantidad KM',
#                     'Alumnos', 'Sectores', 'Escuela', 'URL Mapa'])

#     data = Transporte.objects.all().values_list('patente', 'oferente', 'cantidad_km',
#                                                 'alumnos', 'sectores', 'escuela__nombre', 'url_mapa')
#     for row in data:
#         writer.writerow(row)

#     return response


def export_escuelas_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Escuelas"

    ws.append(['RBD', 'Digito Verificador', 'Nombre'])

    for escuela in Escuela.objects.all():
        ws.append([escuela.rbd, escuela.digito_verificador, escuela.nombre])

    response = HttpResponse(save_virtual_workbook(
        wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=escuelas.xlsx'
    return response


def export_transportes_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Transportes"

    ws.append(['Patente', 'Oferente', 'Cantidad KM', 'Alumnos', 'Sectores', 'Escuela', 'RBD', 'DV', 'URL Mapa'])

    for transporte in Transporte.objects.all():
        ws.append([transporte.patente, transporte.oferente, transporte.cantidad_km, transporte.alumnos, transporte.sectores, transporte.escuela.nombre, transporte.escuela.rbd, transporte.escuela.digito_verificador, transporte.url_mapa])

    response = HttpResponse(save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=transportes.xlsx'
    return response



# def export_escuelas_pdf(request):
#     escuelas = Escuela.objects.all()
#     username = request.user.username
#     date_str = datetime.now().strftime('%d-%m-%Y')

#     template = get_template('informe/escuelas.html')
#     context = {
#         'escuelas': escuelas,
#         'username': username,
#         'date_str': date_str,
#     }
#     html = template.render(context)

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=escuelas.pdf'

#     pisa_status = pisa.CreatePDF(
#         html.encode('utf-8'), dest=response,
#         encoding='utf-8'
#     )

#     if pisa_status.err:
#         return HttpResponse('Error al generar el PDF: %s' % pisa_status.err)

#     return response


# def export_transportes_pdf(request):
#     transportes = Transporte.objects.all()
#     username = request.user.username
#     date_str = datetime.now().strftime('%d-%m-%Y')

#     template = get_template('informe/transportes.html')
#     context = {
#         'transportes': transportes,
#         'username': username,
#         'date_str': date_str,
#     }
#     html = template.render(context)

#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename=transportes.pdf'

#     pisa_status = pisa.CreatePDF(
#         html.encode('utf-8'), dest=response,
#         encoding='utf-8'
#     )

#     if pisa_status.err:
#         return HttpResponse('Error al generar el PDF: %s' % pisa_status.err)

#     return response
