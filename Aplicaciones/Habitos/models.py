from django.db import models
from django.utils import timezone

class Habitos(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    meta_tiempo = models.PositiveIntegerField(default=15, help_text="Meta diaria en minutos")  # 60 minutos predeterminados
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.BooleanField(default=True)  # Activo o Inactivo
    prioridad = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre
    

class RegistroInicio(models.Model):
    habito = models.ForeignKey(Habitos, related_name='registros', on_delete=models.CASCADE)
    fecha_inicio = models.DateTimeField(default=timezone.now)
    tiempo_transcurrido = models.IntegerField(default=0)  # en minutos
    completado = models.BooleanField(default=False)

    def __str__(self):
        return f"Inicio de {self.habito.nombre} en {self.fecha_inicio}"

    def actualizar_progreso(self, tiempo):
        self.tiempo_transcurrido += tiempo
        if self.tiempo_transcurrido >= self.habito.meta_tiempo:
            self.completado = True
        self.save()
