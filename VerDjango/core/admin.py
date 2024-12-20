from django.contrib import admin
from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone_number', 'address', 'user_type']
    search_fields = ['username']
    list_per_page = 5


class LocalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion', 'categoria', 'telefono', 'whatsapp', 'correo', 'dueño']
    search_fields = ('nombre', 'direccion')

    def valoraciones_promedio(self, obj):
        valoraciones = obj.valoraciones.all()
        if valoraciones:
            promedio = valoraciones.aggregate(models.Avg('puntuacion'))['puntuacion__avg']
            return round(promedio, 2) if promedio else 'No valorado'
        return 'No valorado'
    
    valoraciones_promedio.admin_order_field = 'valoraciones'
    valoraciones_promedio.short_description = 'Valoración Promedio'

admin.site.register(Local, LocalAdmin)
admin.site.register(CustomUser, CustomUserAdmin)