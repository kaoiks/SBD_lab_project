import json

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from rest_framework.test import APIClient


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--username')
        parser.add_argument('-p', '--password')
        parser.add_argument('-e', '--email', default='developeremail@mail.com')

    def handle(self, username, password, email, **options):

        if User.objects.filter(username=username).exists():
            raise Exception('Username already exists!')

        if User.objects.filter(email=email).exists():
            raise Exception('User with this email already exists')

        user = User.objects.create_superuser(
            username=username,
            email=email
        )
        user.set_password(password)
        user.save()

        client = APIClient()
        data = {'username': username, 'password': password, 'email': email}
        response = client.post('/auth/login/', data=data)
        tokens = response.json()

        self.stdout.write(json.dumps(tokens))




