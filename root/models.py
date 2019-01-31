from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from datetime import datetime
from .constants import SEXO
from decimal import *


# Asociacion a la cual pertenece un deportista
class Institucion(models.Model):
    nombre = models.CharField(max_length=125, unique=True)
    logo = models.ImageField(
        upload_to='institucion', default='/defautl/default_institucion.png')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse('list-institucion')


# Deporte
class Deporte(models.Model):
    deporte = models.CharField(max_length=45, unique=True)

    def __str__(self):
        return self.deporte


# Categoria
class Categoria(models.Model):
    categoria = models.CharField(max_length=45)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    parametro_mayor_masa_grasa = models.DecimalField(max_digits=3,
                                                     decimal_places=1)
    parametro_menor_masa_grasa = models.DecimalField(max_digits=3,
                                                     decimal_places=1)
    parametro_mayor_masa_muscular = models.DecimalField(max_digits=3,
                                                        decimal_places=1)
    parametro_medio_masa_muscular = models.DecimalField(max_digits=3,
                                                        decimal_places=1)
    parametro_menor_masa_muscular = models.DecimalField(max_digits=3,
                                                        decimal_places=1)

    def __str__(self):
        return self.categoria


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
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL,
                                  null=True, blank=True)
    institucion = models.ForeignKey(
        Institucion, on_delete=models.SET_NULL, null=True, blank=True)
    informacion_extra = models.TextField(null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    def get_absolute_url(self):
        return reverse('detail-deportista', kwargs={'pk': self.pk})

    def get_age(self):
        age = datetime.now().year - self.fecha_nacimiento.year
        return 0 if age < 1 else age


class DeportistaInfo(models.Model):
    deportista = models.OneToOneField(Deportista, on_delete=models.CASCADE)
    dni = models.CharField(max_length=8, null=True, blank=True)
    lugar_nacimiento = models.CharField(max_length=45, null=True, blank=True)
    direccion = models.TextField(null=True, blank=True)
    nombre_padre = models.CharField(max_length=200, null=True, blank=True)
    nombre_madre = models.CharField(max_length=200, null=True, blank=True)
    telefono = models.CharField(max_length=9, null=True, blank=True)
    celular = models.CharField(max_length=9, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    contacto_emergencia = models.CharField(
        max_length=45, null=True, blank=True)
    contacto_emergencia_numero = models.CharField(
        max_length=9, null=True, blank=True)
    eduacion = models.CharField(max_length=120, null=True, blank=True)
    observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.deportista


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
        return self.deportista.__str__()

    def get_absolute_url(self):
        return reverse('detail-deportista', kwargs={'pk': self.deportista.pk})

    def get_sum_pliegues(self):
        sum_pliegues = self.triceps + self.subescapular + self.supraespinal + \
               self.abdominales + self.muslo_medio + self.pliege_pierna
        return sum_pliegues.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_grasa_corporal(self):
        grasa_corporal = ((Decimal(0.1051) * self.get_sum_pliegues()) +
                          (Decimal(2.585))) / Decimal(100)
        return grasa_corporal.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_masa_magra(self):
        masa_magra = self.peso_bruto - (
                self.peso_bruto * self.get_grasa_corporal())
        return masa_magra.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_peso_ideal_menor(self):
        peso_ideal_menor = self.get_masa_magra() / Decimal(0.95)
        return peso_ideal_menor.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_peso_ideal_mayor(self):
        peso_ideal_mayor = self.get_masa_magra() / Decimal(0.91)
        return peso_ideal_mayor.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_indice_masa_corporal(self):
        indice_masa_corporal = self.peso_bruto / \
                               Decimal(pow(float(self.estatura)/100.0, 2))
        return indice_masa_corporal.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_indice_sustancia_activa(self):
        indice_sustancia_activa = (self.get_masa_magra() * Decimal(100000)) / \
                                  (Decimal(pow(float(self.estatura), 3))
                                   .quantize(Decimal('.01'),
                                             rounding=ROUND_UP))
        return indice_sustancia_activa.quantize(Decimal('.01'),
                                                rounding=ROUND_UP)

    def get_indice_cintaura_cadera(self):
        indice_cintaura_cadera = self.cintura / self.cadera
        return indice_cintaura_cadera.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_indice_citura_talla(self):
        indice_citura_talla = self.cintura / self.estatura
        return indice_citura_talla.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_endomorfismo(self):
        x = (self.triceps + self.subescapular + self.supraespinal) * \
            Decimal(170.18) / self.estatura
        endomorfismo = (Decimal(0.1451) * x) - \
               (Decimal(0.00068) * Decimal(pow(float(x), 2))) + \
               (Decimal(0.0000014) * Decimal(pow(float(x), 3))) - \
               (Decimal(0.7182))
        return endomorfismo.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_mesomorfismo(self):
        E = self.humeral
        K = self.femoral
        A = self.brazo_flexionado - (self.triceps / Decimal(10))
        C = self.perimetro_pantorrilla - (self.pliege_pierna / Decimal(10))
        H = self.estatura
        mesomorfismo = (Decimal(0.858) * E) + (Decimal(0.601) * K) + \
                       (Decimal(0.188) * A) + (Decimal(0.161) * C) - \
                       (Decimal(0.131) * H) + Decimal(4.5)
        return mesomorfismo.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_ectomorfismo(self):
        rpi = self.estatura / Decimal((pow(float(self.peso_bruto), 0.3333)))
        ectomorfismo = None
        if rpi > Decimal(40.75):
            ectomorfismo = (Decimal(0.732) * rpi) - Decimal(28.58)
        elif Decimal(38.25) <= rpi <= Decimal(40.75):
            ectomorfismo = (Decimal(0.463) * rpi) - Decimal(17.63)
        elif rpi < Decimal(38.25):
            ectomorfismo = Decimal(0.1)
        return ectomorfismo.quantize(Decimal('.01'), rounding=ROUND_UP)

    def get_caracterizacion(self):
        endo = self.get_endomorfismo()
        meso = self.get_mesomorfismo()
        ecto = self.get_ectomorfismo()
        metrics = [endo, meso, ecto]
        if abs(endo-meso) < Decimal(1) and \
                abs(endo-ecto) < Decimal(1) and \
                abs(meso-ecto) < Decimal(1):
            return 'Central'
        elif max(metrics) == endo:
            if (ecto - meso) > Decimal(0.5):
                return 'Endo ectomórfico'
            elif abs(ecto - meso) < Decimal(0.5):
                return 'Endo balanceado'
            elif (meso - ecto) > Decimal(0.5):
                return 'Endo mesomórfico'
        elif min(metrics) == ecto and abs(endo - meso) < Decimal(0.5):
            return 'Endomorfo mesomorfo'
        elif max(metrics) == meso:
            if (endo - ecto) > Decimal(0.5):
                return 'Meso endomórfico'
            elif abs(endo - ecto) < Decimal(0.5):
                return 'Meso balanceado'
            elif (ecto - endo) > Decimal(0.5):
                return 'Meso ectomórfico'
        elif min(metrics) == endo and abs(ecto - meso) < Decimal(0.5):
            return 'Ectomorfo mesomorfo'
        elif max(metrics) == ecto:
            if (meso - endo) > Decimal(0.5):
                return 'Ecto mesomórfico'
            elif abs(meso - endo) < Decimal(0.5):
                return 'Ecto balanceado'
            elif (endo - meso) > Decimal(0.5):
                return 'Ecto endomórfico'
        elif min(metrics) == meso and abs(ecto - endo) < Decimal(0.5):
            return 'Ectomorfo endomorfo'

    def get_observacion_masa_grasa(self):
        sum_6_pliegues = self.get_sum_pliegues()
        if sum_6_pliegues > Decimal(65):
            return 'red', 'Muy elevada masa grasa'
        elif Decimal(51) < sum_6_pliegues < Decimal(65):
            return 'yellow', 'Elevada masa grasa'
        else:
            return 'blue', 'Adecuada masa grasa'

    def get_observacion_masa_muscular(self):
        imc = self.get_indice_masa_corporal()
        if imc < Decimal(16.3):
            return 'red', 'Muy escasa masa muscular'
        elif imc < Decimal(18.0):
            return 'yellow', 'Escasa masa muscular'
        elif Decimal(18.0) < imc < Decimal(20.6):
            return 'blue', 'Adecuada Musculatura'
        elif imc > Decimal(20.6):
            return 'orange', 'Elevada Musculatura'

