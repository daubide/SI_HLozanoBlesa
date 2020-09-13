# Generated by Django 3.0.7 on 2020-08-17 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processmining', '0002_remove_profesional_area_prof'),
    ]

    operations = [
        migrations.AddField(
            model_name='profesional',
            name='area_prof',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='processmining.AREAPROFESIONAL'),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='origen_paciente',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='sexo_paciente',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AlterField(
            model_name='profesional',
            name='tipo_profesional',
            field=models.CharField(default='', max_length=150),
        ),
    ]