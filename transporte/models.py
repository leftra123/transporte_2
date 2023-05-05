from django.db import models

class Escuela(models.Model):
    rbd = models.IntegerField(primary_key=True)
    digito_verificador = models.CharField(max_length=1)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Transporte(models.Model):
    patente = models.CharField(max_length=10, primary_key=True)
    oferente = models.CharField(max_length=100)
    cantidad_km = models.FloatField()
    alumnos = models.PositiveIntegerField()
    sectores = models.CharField(max_length=200)
    escuela = models.ForeignKey(Escuela, on_delete=models.CASCADE)
    url_mapa = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.oferente} - {self.patente}"
