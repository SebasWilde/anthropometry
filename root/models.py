from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from datetime import datetime
from .constants import SEXO


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
    sexo = models.CharField(max_length=2, choices=SEXO)
    foto = models.ImageField(
        upload_to='deportista', default='/defautl/default_user.png')
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


# class DeportistaInfo(models.Model):
#     deportista = models.OneToOneField(Deportista, on_delete=models.CASCADE)
#     dni = models.CharField(max_length=8, null=True, blank=True)
#     lugar_nacimiento = models.CharField(max_length=45, null=True, blank=True)
#     direccion = models.TextField(null=True, blank=True)
#     nombre_padre = models.CharField(max_length=200, null=True, blank=True)
#     nombre_madre = models.CharField(max_length=200, null=True, blank=True)
#     telefono = models.CharField(max_length=9, null=True, blank=True)
#     celular = models.CharField(max_length=9, null=True, blank=True)
#     email = models.EmailField(null=True, blank=True)
#     contacto_emergencia_numero = models.CharField(
#         max_length=9, null=True, blank=True)
#     contacto_emergencia = models.CharField(
#         max_length=45, null=True, blank=True)
#     eduacion = models.CharField(max_length=120, null=True, blank=True)
#     observaciones = models.TextField(null=True, blank=True)
#
#     def __str__(self):
#         return self.deportista


# Medidas que se toman
class Medida(models.Model):
    deportista = models.ForeignKey(Deportista, on_delete=models.CASCADE)
    fecha_registro = models.DateField(
        default=now, blank=True)
    peso_bruto = models.DecimalField(max_digits=4, decimal_places=1)
    estatura = models.DecimalField(max_digits=4, decimal_places=1)
    talla_sentado = models.DecimalField(max_digits=4, decimal_places=1)
    cintura = models.DecimalField(max_digits=4, decimal_places=1)
    cadera = models.DecimalField(max_digits=4, decimal_places=1)
    humeral = models.DecimalField(max_digits=3, decimal_places=1)
    femoral = models.DecimalField(max_digits=3, decimal_places=1)
    brazo_flexionado = models.DecimalField(max_digits=3, decimal_places=1)
    perimetro_pantorrilla = models.DecimalField(max_digits=3, decimal_places=1)
    triceps = models.DecimalField(max_digits=3, decimal_places=1)
    subescapular = models.DecimalField(max_digits=3, decimal_places=1)
    biceps = models.DecimalField(max_digits=3, decimal_places=1)
    suprailiaco = models.DecimalField(max_digits=3, decimal_places=1)
    supraespinal = models.DecimalField(max_digits=3, decimal_places=1)
    abdominales = models.DecimalField(max_digits=3, decimal_places=1)
    muslo_medio = models.DecimalField(max_digits=3, decimal_places=1)
    pliege_pierna = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return self.deportista

    def get_absolute_url(self):
        return reverse('detail-deportista', kwargs={'pk': self.deportista.pk})

    def get_sum_plieges(self):
        return self.triceps + self.subescapular + self.supraespinal + \
               self.abdominales + self.muslo_medio + self.pliege_pierna

    def get_grasa_corporal(self):
        return ((0.1051 * self.get_sum_plieges()) + 2.585) / 100

    def get_masa_magra(self):
        return self.peso_bruto - (self.peso_bruto * self.get_grasa_corporal())

    def get_peso_ideal_menor(self):
        return self.get_masa_magra() / 0.95

    def get_peso_ideal_mayor(self):
        return self.get_masa_magra() / 0.91

    def get_indice_masa_corporal(self):
        return self.peso_bruto / (pow(float(self.estatura), 2))

    def get_indice_sustancia_activa(self):
        return (self.get_masa_magra() * 100000) / pow(float(self.estatura), 3)

    def get_indice_cintaura_cadera(self):
        return self.cintura / self.cadera

    def get_indice_citura_talla(self):
        return self.cintura / self.estatura

    def get_endomorfismo(self):
        x = (self.triceps + self.subescapular + self.supraespinal) * \
            170.18 / self.estatura
        return (0.1451 * x) - (0.00068 * pow(float(x), 2)) + \
               (0.0000014 * pow(float(x), 3)) - 0.7182

    def get_mesomorfismo(self):
        return (0.858 * self.humeral) + (0.601 * self.femoral) + \
               (0.188 * (self.brazo_flexionado - (self.triceps / 10))) + \
               (0.161 * (self.perimetro_pantorrilla - (self.pliege_pierna / 10))) \
               + (0.131 * self.estatura) - 4.5

    def get_ectomorfismo(self):
        rpi = self.estatura / (pow(float(self.peso_bruto), 0.3333))
        if rpi > 40.75:
            return (0.732 * rpi) - 28.58
        elif 38.25 <= rpi <= 40.75:
            return (0.463 * rpi) - 17.63
        elif rpi < 38.25:
            return 0.1

    def get_caracterizacion(self):
        endo = self.get_endomorfismo()
        meso = self.get_mesomorfismo()
        ecto = self.get_ectomorfismo()
        metrics = [endo, meso, ecto]
        if abs(endo-meso) < 1 and abs(endo-ecto) < 1 and abs(meso-ecto) < 1:
            return 'Central'
        elif max(metrics) == endo:
            if (ecto - meso) > 0.5:
                return 'Endo ectomórfico'
            elif abs(ecto - meso) < 0.5:
                return 'Endo balanceado'
            elif (meso - ecto) > 0.5:
                return 'Endo mesomórfico'
        elif min(metrics) == ecto and abs(endo - meso) < 0.5:
            return 'Endomorfo mesomorfo'
        elif max(metrics) == meso:
            if (endo - ecto) > 0.5:
                return 'Meso endomórfico'
            elif abs(endo - ecto) < 0.5:
                return 'Meso balanceado'
            elif (ecto - endo) > 0.5:
                return 'Meso ectomórfico'
        elif min(metrics) == endo and abs(ecto - meso) < 0.5:
            return 'Ectomorfo mesomorfo'
        elif max(metrics) == ecto:
            if (meso - endo) > 0.5:
                return 'Ecto mesomórfico'
            elif abs(meso - endo) < 0.5:
                return 'Ecto balanceado'
            elif (endo - meso) > 0.5:
                return 'Ecto endomórfico'
        elif min(metrics) == meso and abs(ecto - endo) < 0.5:
            return 'Ectomorfo endomorfo'

    def get_observacion_masa_grasa(self):
        sum_6_pliegues = self.get_sum_plieges()
        if sum_6_pliegues > 65:
            return 'red', 'Muy elevada masa grasa'
        elif 51 < sum_6_pliegues < 65:
            return 'yellow', 'Elevada masa grasa'
        else:
            return 'blue', 'Adecuada masa grasa'

    def get_observacion_masa_muscular(self):
        imc = self.get_indice_masa_corporal()
        if imc < 16.3:
            return 'red', 'Muy escasa masa muscular'
        elif imc < 18.0:
            return 'yellow', 'Escasa masa muscular'
        elif 18.0 < imc < 20.6:
            return 'blue', 'Adecuada Musculatura'
        elif imc > 20.6:
            return 'orange', 'Elevada Musculatura'


