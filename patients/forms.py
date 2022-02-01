from django.forms import ModelForm
from rdv.models import Patients
from django import forms

class PatientForm (ModelForm):
    prenom = forms.CharField(error_messages={'required': 'Obligatoire'})
    nom = forms.CharField(error_messages={'required': 'Obligatoire'})
    cin = forms.CharField(error_messages={'required': 'Obligatoire'})

    class Meta:
        model = Patients
        fields = '__all__'
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'cin': 'CIN',
            'email': 'E-mail',
            'telephone': 'Téléphone',
            'date_naissance': 'Date de naissance',
        }