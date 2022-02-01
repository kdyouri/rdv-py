# Generated by Django 4.0 on 2022-01-15 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rdv', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='date_naissance',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='patients',
            name='email',
            field=models.EmailField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='telephone',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
