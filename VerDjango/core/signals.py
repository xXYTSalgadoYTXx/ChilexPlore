from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group
from django.dispatch import receiver

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Cliente normal')
    Group.objects.get_or_create(name='Cliente dueño de negocios')
    Group.objects.get_or_create(name='Administrador')
