from django.forms import ModelForm
from rdv.models import Rendezvous
from django import forms

class RendezvousForm (ModelForm):
    patient_id = forms.IntegerField(error_messages={'required': 'Obligatoire'})
    date_heure = forms.DateTimeField(error_messages={'required': 'Obligatoire'})
    duree = forms.IntegerField(error_messages={'required': 'Obligatoire'})

    class Meta:
        model = Rendezvous
        fields = ('date_heure', 'duree', 'remarque')