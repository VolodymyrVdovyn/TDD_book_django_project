from django.conf import settings
from django.contrib import auth
from django.contrib.sessions.backends.db import SessionStore
from django.core.management import BaseCommand

User = auth.get_user_model()


def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[auth.SESSION_KEY] = user.pk
    session[auth.BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("email")

    def handle(self, *args, **options):
        session_key = create_pre_authenticated_session(options["email"])
        self.stdout.write(session_key)
