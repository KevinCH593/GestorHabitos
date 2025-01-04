# Generated by Django 5.1.3 on 2024-12-21 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Habitos', '0003_habitos_estado_habitos_prioridad'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habitos',
            name='meta_horas',
        ),
        migrations.RemoveField(
            model_name='progreso',
            name='horas_registradas',
        ),
        migrations.AddField(
            model_name='habitos',
            name='meta_tiempo',
            field=models.PositiveIntegerField(default=15, help_text='Meta diaria en minutos'),
        ),
        migrations.AddField(
            model_name='progreso',
            name='tiempo_registrado',
            field=models.PositiveIntegerField(default=15, help_text='Tiempo registrado en minutos'),
            preserve_default=False,
        ),
    ]
