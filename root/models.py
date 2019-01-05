from django.db import models
from django.urls import reverse
from datetime import datetime

# Asociaciona la cual pertenece un deportista
class Asociacion(models.Model):
    nombre = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.nombre


# Deporte
class Deporte(models.Model):
    deporte = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.deporte


# Deportista
class Deportista(models.Model):
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(
        upload_to='deportista', default='../media/defautl/default_user.png')
    deporte = models.ForeignKey(
        Deporte, on_delete=models.SET_NULL, null=True, blank=True)
    asociacion = models.ForeignKey(
        Asociacion, on_delete=models.SET_NULL, null=True, blank=True)
    informacion_extra = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    def get_absolute_url(self):
        return reverse('detail-deportista', kwargs={'pk': self.pk})

    def get_age(self):
        age = datetime.now().year - self.fecha_nacimiento.year
        return 0 if age < 1 else age
