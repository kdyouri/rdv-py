from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection
from django.conf import settings
from rdv.models import Patients
from .forms import PatientForm

@login_required
def index(request):
    # Ordre :
    order_by = request.GET.get('sort', 'nom')
    queryset = Patients.objects.all().order_by(order_by)

    # Pagination :
    paginator = Paginator(queryset, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'order_by': order_by,
        'conn': connection,
        'debug': settings.DEBUG
    }
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        context['layout'] = 'layouts/ajax.html'
    else:
        context['layout'] = 'layouts/default.html'
        context['tab'] = 'patients'

    return render(request, 'Patients/index.html', context)

@login_required
def add(request):
    context = {}
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/patients')
        else:
            context['error_message'] = 'Patient n’a pas pu être ajouté! Veuillez réessayer.'
    else:
        form = PatientForm()
    context['form'] = form

    return render(request, 'Patients/add.html', context)

@login_required
def edit(request, id):
    patient = get_object_or_404(Patients, pk=id)
    form = PatientForm(request.POST or None, instance=patient)
    context = {}

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/patients')
        else:
            context['error_message'] = 'Patient n’a pas pu être modifié! Veuillez réessayer.'

    context['form'] = form

    return render(request, 'Patients/edit.html', context)

@login_required
def delete(request, id):
    patient = get_object_or_404(Patients, pk=id)
    patient.delete()
    return redirect('/patients')