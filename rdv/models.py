from ast import alias
from django.db import models

class Patients(models.Model) :
    id = models.AutoField(primary_key=True)
    prenom = models.CharField(max_length=50)
    nom = models.CharField(max_length=50)
    cin = models.CharField(max_length=10)
    email = models.EmailField(max_length=255, blank=True)
    telephone = models.CharField(max_length=10, blank=True)
    date_naissance = models.DateField(null=True, blank=True)

class Rendezvous(models.Model) :
    id = models.AutoField(primary_key=True)
    patient_id = models.ForeignKey(Patients, on_delete=models.CASCADE)
    date_heure = models.DateTimeField()
    duree = models.IntegerField()
    remarque = models.TextField(blank=True)

