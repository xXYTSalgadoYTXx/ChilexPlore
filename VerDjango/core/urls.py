from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', mapa_locales, name='index'),

    path('mapa_locales/', mapa_locales, name='mapa_locales'),

    path('login/', login_view, name='login'),
    path('registro/', registro, name='registro'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('mis_locales/', mis_locales, name='mis_locales'),
    path('crear_local/', crear_local, name='crear_local'),
    path('modificar_local/<int:pk>/', modificar_local, name='modificar_local'),
    path('eliminar_local/<int:pk>/', eliminar_local, name='eliminar_local'),

    path('favoritos/', ver_favoritos, name='ver_favoritos'),

    path('perfil/', perfil, name='perfil'),
    path('editar_perfil/', editar_perfil, name='editar_perfil'),

    path('toggle_favorito/<int:local_id>/', toggle_favorito, name='toggle_favorito'),
    path('valorar_local/<int:local_id>/', valorar_local, name='valorar_local'),

    path('reportar-bug/', report_bug, name='report_bug'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)