from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, cd
import random

RERO_URL = "git@github.com:VolodymyrVdovyn/TDD_book_django_project.git"


def _create_project_folder(project_folder):
    run(f"mkdir -p {project_folder}")


def _get_latest_project_from_git():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {RERO_URL} .")
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _update_settings(site_name):
    settings_path = "./src/config/settings.py"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS = .+$", f'ALLOWED_HOSTS = ["{site_name}"]')
    secret_key_file = "./src/config/secret_key.py"
    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, "\nfrom .secret_key import SECRET_KEY")


def _update_venv():
    if not exists("./venv/bin/pip"):
        run(f"python3 -m venv venv")
        run(f"./venv/bin/pip install -U pip")
    run(f"./venv/bin/pip install -r requirements.txt")


def _update_static_files():
    run(f"./venv/bin/python ./src/manage.py collectstatic --noinput")


def _update_database():
    run(f"mkdir -p database")
    run(f"./venv/bin/python ./src/manage.py migrate --noinput")


def __configurate_nginx_and_gunicorn(site_name):
    run(f"s/SITENAME/{site_name}/g ")


def deploy():
    project_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {project_folder}")

    with cd(project_folder):
        _get_latest_project_from_git()
        _update_settings(env.host)
        _update_venv()
        _update_static_files()
        _update_database()
