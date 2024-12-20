from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db.models import ManyToManyField
from .validators import *

# models.py

class Local(models.Model):
    CATEGORIAS = [
        ('Turismo', 'Turismo'),
        ('Restaurante', 'Restaurante'),
        ('Hospedaje', 'Hospedaje'),
        ('Aventura', 'Turismo de Aventura'),
        ('Natural', 'Lugar Natural'),
        ('Cultural', 'Patrimonio Cultural'),
    ]

    nombre = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255)
    latitud = models.FloatField()
    longitud = models.FloatField()
    categoria = models.CharField(max_length=50, choices=CATEGORIAS)    
    telefono = models.CharField(max_length=20, blank=True, null=True, validators=[validate_telefono])
    whatsapp = models.CharField(max_length=20, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    imagen = models.ImageField(upload_to='locales/')
    dueño = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='locales')

    def __str__(self):
        return self.nombre

    
class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    user_type = models.CharField(max_length=50, choices=[('business', 'Dueño de Negocio'), ('customer', 'Cliente')], default='customer')
    favoritos = ManyToManyField(Local, related_name='favorito_de', blank=True)
    
class Valoracion(models.Model):
    local = models.ForeignKey(Local, related_name='valoraciones', on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Valoración de {self.local.nombre} - Puntuación {self.puntuacion}"


class Imagen(models.Model):
    local = models.ForeignKey(Local, related_name='imagenes_local', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='locales_imagenes/')

    def __str__(self):
        return f"Imagen para el local {self.local.nombre}"


class Bug(models.Model):

    CATEGORIASBUG = [
        ('Error/Bug', 'Error/Bug'),
        ('Mejora', 'Mejora'),
        ('Sugerencia', 'Nueva Funcionalidad'),
    ]
    CATEGORIASPRIO = [
        ('Baja', 'Baja'),
        ('Media', 'Madia'),
        ('Alta', 'Alta'),
    ]

    descripcion = models.CharField(max_length=255, blank=True, null=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIASBUG)
    prioridad = models.CharField(max_length=50, choices=CATEGORIASPRIO)
    captura = models.ImageField(upload_to='bugimagenes/', blank=True, null=True)
    contacto = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.descripcion