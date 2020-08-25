from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create super user'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        qs = User.objects.filter(username='admin')
        if not qs.exists():
            user = User.objects.create_superuser(
                'admin',
                'admin@gmail.com',
                'admin'
            )
