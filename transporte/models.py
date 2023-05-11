from django.db import models

class Escuela(models.Model):
    id = models.AutoField(primary_key=True)  
    rbd = models.IntegerField(unique=True) 
    digito_verificador = models.CharField(max_length=1)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Oferente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)  

    def __str__(self):
        return self.nombre

class Chofer(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12)  
    oferente = models.ForeignKey(Oferente, on_delete=models.CASCADE, related_name='choferes')

    def __str__(self):
        return self.nombre

class Transporte(models.Model):
    id = models.AutoField(primary_key=True)
    patente = models.CharField(max_length=10)
    oferente = models.ForeignKey(Oferente, on_delete=models.CASCADE)
    chofer = models.ForeignKey(Chofer, on_delete=models.CASCADE)
    cantidad_km = models.FloatField()
    alumnos = models.PositiveIntegerField()
    sectores = models.CharField(max_length=200)
    escuela = models.ManyToManyField(Escuela)  
    url_mapa = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.oferente} - {self.patente}"