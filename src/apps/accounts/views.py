from accounts.models import Token
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse

SEND_MAIL_SUCCESS_MESSAGE = "Check your email, you'll find a message with a link that will log you into the site."
SEND_MAIL_SUBJECT = "Your login link for Superlists"


def send_login_email(request):
    email = request.POST["email"]
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(reverse("login", kwargs={"token": token.uid}))

    send_mail(
        subject=SEND_MAIL_SUBJECT,
        message=f"Use this link to log in:\n\n{url}",
        from_email="noreply@superlists",
        recipient_list=[email],
    )

    messages.success(
        request=request,
        message=SEND_MAIL_SUCCESS_MESSAGE,
    )
    return redirect("/")


def login(request, token):
    user = auth.authenticate(uid=token)
    if user:
        auth.login(request, user)
    return redirect("/")


def logout(request):
    auth.logout(request)
    return redirect("/")
