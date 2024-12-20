from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse

from .models import *
from .forms import *

import json


def index(request):
    return render(request, 'core/index.html')


@login_required
def mapa_locales(request):
    locales = Local.objects.all().prefetch_related('valoraciones__usuario')
    return render(request, 'core/mapa_locales.html', {'coordenadas': locales})

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'core/registro.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mapa_locales')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})


@login_required
def mis_locales(request):
    locales = Local.objects.filter(dueño=request.user)
    return render(request, 'core/mis_locales.html', {'locales': locales})

@login_required
def crear_local(request):
    if request.method == 'POST':
        form = LocalForm(request.POST, request.FILES)
        if form.is_valid():
            local = form.save(commit=False)
            local.dueño = request.user
            local.save()
            form.save_m2m()
            return redirect('mapa_locales') 
    else:
        form = LocalForm()
    return render(request, 'core/crear_local.html', {'form': form})

@login_required
def modificar_local(request, pk):
    local = get_object_or_404(Local, pk=pk, dueño=request.user)
    if request.method == 'POST':
        form = LocalForm(request.POST, request.FILES, instance=local)
        if form.is_valid():
            form.save()
            return redirect('mis_locales')
    else:
        form = LocalForm(instance=local)
    return render(request, 'core/modificar_local.html', {'form': form, 'local': local})

@login_required
def eliminar_local(request, pk):
    local = get_object_or_404(Local, pk=pk, dueño=request.user)
    if request.method == 'POST':
        local.delete()
        messages.success(request, 'El local ha sido eliminado exitosamente.')
        return redirect('mis_locales')
    return render(request, 'core/eliminar_local.html', {'local': local})


@login_required
def perfil(request):
    return render(request, 'core/perfil.html', {'user': request.user})

@login_required
def editar_perfil(request):
    user = request.user
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('perfil')
    else:
        form = EditarPerfilForm(instance=user)
    return render(request, 'core/editar_perfil.html', {'form': form})


@login_required
def toggle_favorito(request, local_id):
    if request.method == 'POST':
        local = get_object_or_404(Local, id=local_id)
        
        usuario = request.user

        if local in usuario.favoritos.all():
            usuario.favoritos.remove(local)
            message = 'Local quitado de favoritos'
            status = 'removed'
        else:
            usuario.favoritos.add(local)
            message = 'Local agregado a favoritos'
            status = 'added'

        return JsonResponse({'status': status, 'message': message})

    return JsonResponse({'status': 'error', 'message': 'No autorizado o sesión no iniciada'}, status=401)

def ver_favoritos(request):
    if request.user.is_authenticated:
        user = request.user
        favoritos = user.favoritos.all()
        return render(request, 'core/favoritos.html', {'favoritos': favoritos})
    else:
        return redirect('login_view')

def obtener_valoraciones(request, local_id):
    try:
        local = Local.objects.get(id=local_id)
        valoraciones = list(local.valoraciones.values('puntuacion', 'comentario'))
        return JsonResponse({'valoraciones': valoraciones})
    except Local.DoesNotExist:
        return JsonResponse({'error': 'Local no encontrado.'}, status=404)

@login_required
@csrf_exempt
def valorar_local(request, local_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            puntuacion = data.get('puntuacion')
            comentario = data.get('comentario')

            if not puntuacion or not comentario:
                return JsonResponse({'error': 'Faltan datos para la valoración.'}, status=400)

            local = get_object_or_404(Local, id=local_id)

            valoracion_existente = Valoracion.objects.filter(local=local, usuario=request.user).first()

            if valoracion_existente:
                valoracion_existente.puntuacion = puntuacion
                valoracion_existente.comentario = comentario
                valoracion_existente.save()

                return JsonResponse({'message': 'Valoración actualizada correctamente.'})
            else:
                Valoracion.objects.create(local=local, usuario=request.user, puntuacion=puntuacion, comentario=comentario)

                return JsonResponse({'message': 'Valoración enviada correctamente.'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido.'}, status=405)

@login_required
@csrf_exempt
def report_bug(request):
    if request.method == 'POST':
        form = BugForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('mapa_locales')
    else:
        form = BugForm()

    return render(request, 'core/report_bug.html', {'form': form})