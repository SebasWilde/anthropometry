from django.db import models


class Deportista(models.Model):
    nombres = models.CharField(max_length=45)
    apellidos = models.CharField(max_length=45)
    fecha_nacimiento = models.DateField()
    foto = models.ImageField(upload_to='deportista', default='../media/defautl/default_user.png')

    def __str__(self):
        return self.nombres + self.apellidos
