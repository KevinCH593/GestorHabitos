# Generated by Django 5.1.3 on 2024-12-25 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Habitos', '0006_registrohabito'),
    ]

    operations = [
        migrations.AddField(
            model_name='habitos',
            name='progreso_objetivo',
            field=models.PositiveIntegerField(default=100, help_text='Progreso objetivo'),
        ),
    ]
