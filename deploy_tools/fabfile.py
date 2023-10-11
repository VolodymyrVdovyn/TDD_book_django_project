import os
import random
import re

from fabric.api import cd, env, local, run, sudo
from fabric.contrib.files import append, exists, sed

RERO_URL = "git@github.com:VolodymyrVdovyn/TDD_book_django_project.git"


def _set_env_password():
    server_sudo_password_file = f'{local("pwd", capture=True)}/server_sudo_password.txt'

    if not os.path.exists(server_sudo_password_file):
        raise Exception("Server sudo password file is not exists")

    with open(server_sudo_password_file, "r") as file:
        text = file.read()
    pattern = r'SERVER_SUDO_PASSWORD = "(.*?)"'
    match = re.search(pattern, text)
    if not match:
        raise Exception("SERVER_SUDO_PASSWORD not exists in file server_sudo_password.txt")

    value = match.group(1)
    env.password = value


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
    sed_command = f'sed "s/SITENAME/{site_name}/g" ./deploy_tools/nginx.template.conf'
    tee_command = f"tee /etc/nginx/sites-available/{site_name}"

    sudo(f"{sed_command} | {tee_command}")

    sudo(f"ln -sf /etc/nginx/sites-available/{site_name}  /etc/nginx/sites-enabled/{site_name}")

    sed_command = f'sed "s/SITENAME/{site_name}/g" ./deploy_tools/gunicorn-systemd.template.service'
    tee_command = f"tee /etc/systemd/system/gunicorn-{site_name}.service"
    sudo(f"{sed_command} | {tee_command}")

    sudo("systemctl daemon-reload")
    sudo("systemctl reload nginx")
    sudo(f"systemctl enable gunicorn-{site_name}")
    sudo(f"systemctl restart gunicorn-{site_name}")


def deploy():
    _set_env_password()
    project_folder = f"/home/{env.user}/sites/{env.host}"
    run(f"mkdir -p {project_folder}")

    with cd(project_folder):
        _get_latest_project_from_git()
        _update_settings(env.host)
        _update_venv()
        _update_static_files()
        _update_database()
        __configurate_nginx_and_gunicorn(env.host)
