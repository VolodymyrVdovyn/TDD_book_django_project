from fabric.api import run
from fabric.context_managers import settings


def _get_manage_py(host):
    return f"~/sites/{host}/venv/bin/python ~/sites/{host}/src/manage.py"


def reset_database(host):
    manage_py = _get_manage_py(host)
    with settings(host_string=f"volo@{host}"):
        run(f"{manage_py} flush --noinput")


def create_session_on_server(host, email):
    manage_py = _get_manage_py(host)
    with settings(host_string=f"volo@{host}"):
        session_key = run(f"{manage_py} create_session {email}")
        return session_key.strip()
