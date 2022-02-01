from django.forms import ModelForm
from django.contrib.auth.models import User
from django import forms

class UserForm (ModelForm):
    username = forms.CharField(error_messages={'required': 'Obligatoire', 'unique': 'Un utilisateur avec ce pseudo existe déjà'})
    password = forms.CharField(error_messages={'required': 'Obligatoire'})
    email = forms.CharField(error_messages={'required': 'Obligatoire'})
    first_name = forms.CharField(error_messages={'required': 'Obligatoire'})
    last_name = forms.CharField(error_messages={'required': 'Obligatoire'})
    date_joined = forms.DateField(error_messages={'required': 'Obligatoire'})

    class Meta:
        model = User
        fields = '__all__'
