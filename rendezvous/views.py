from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection
from django.conf import settings
from http.client import HTTPResponse
import datetime
from json import JSONEncoder
from rdv.models import Rendezvous, Patients
from .forms import RendezvousForm

@login_required
def index(request):
    context = {
        'conn': connection,
        'debug': settings.DEBUG
    }
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        context['layout'] = 'layouts/ajax.html'
    else:
        context['layout'] = 'layouts/default.html'
        context['tab'] = 'rendezvous'

    return render(request, 'Rendezvous/index.html', context)

@login_required
def feed(request):
    start = request.GET.get('start')
    end = request.GET.get('end')

    q = Rendezvous.objects.all().filter(date_heure__gte=start)
    q.filter(date_heure__lte=end)
    
    data = []
    for rendezvous in Rendezvous.objects.all():
        data.append({
            "id": rendezvous.id,
            "title": rendezvous.patient_id.prenom + ' ' + rendezvous.patient_id.nom,
            "start": rendezvous.date_heure,
            "end": rendezvous.date_heure + datetime.timedelta(minutes=rendezvous.duree)
        })

    return JsonResponse(data, safe=False)

@login_required
def add(request):
    context = {}
    if request.method == 'POST':
        form = RendezvousForm(request.POST)
        if form.is_valid():
            rendezvous = form.save(commit=False)
            rendezvous.patient_id = Patients.objects.filter(id=request.POST.get('patient_id'))[0]
            rendezvous.save()
            return redirect('/rendezvous')
        else:
            context['error_message'] = 'Rendez-vous n’a pas pu être ajouté! Veuillez réessayer.'
    else:
        start = request.GET.get('start')
        end = request.GET.get('end')
        defaults = {}
        if start and end:
            dt_start = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S.000Z')
            dt_end = datetime.datetime.strptime(end, '%Y-%m-%dT%H:%M:%S.000Z')
            timedelta = dt_end - dt_start
            defaults = {
                "date_heure": dt_start,
                "duree": int(timedelta.total_seconds() / 60)
            }
        form = RendezvousForm(initial=defaults)

    context['form'] = form
    context['patients'] = Patients.objects.all()

    return render(request, 'Rendezvous/add.html', context)

@login_required
def edit(request, id):
    rendezvous = get_object_or_404(Rendezvous, pk=id)
    form = RendezvousForm(request.POST or None, instance=rendezvous, initial={'patient_id': rendezvous.patient_id.id})
    context = {}

    if request.method == 'POST':
        if form.is_valid():
            rendezvous = form.save(commit=False)
            rendezvous.patient_id = Patients.objects.filter(id=request.POST.get('patient_id'))[0]
            rendezvous.save()
            return redirect('/rendezvous')
        else:
            context['error_message'] = 'Rendez-vous n’a pas pu être modifié! Veuillez réessayer.'

    context['form'] = form
    context['patients'] = Patients.objects.all()
    context['rendezvous_id'] = id

    return render(request, 'Rendezvous/edit.html', context)

@login_required
def delete(request, id):
    rendezvous = get_object_or_404(Rendezvous, pk=id)
    rendezvous.delete()
    return redirect('/rendezvous')