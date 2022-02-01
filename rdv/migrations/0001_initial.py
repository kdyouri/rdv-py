# Generated by Django 4.0 on 2022-01-03 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('prenom', models.CharField(max_length=50)),
                ('nom', models.CharField(max_length=50)),
                ('cin', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=255)),
                ('telephone', models.CharField(max_length=10)),
                ('date_naissance', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Rendezvous',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_heure', models.DateTimeField()),
                ('duree', models.IntegerField()),
                ('remarque', models.TextField()),
                ('patient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rdv.patients')),
            ],
        ),
    ]