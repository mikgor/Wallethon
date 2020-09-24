import os
import shutil

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
application = get_wsgi_application()

from django.core.management import call_command


def make_migrations(clear_migrations=False):
    path = os.getcwd() + '/apps'

    apps = ['main', 'apps/stocks/markets', 'apps/stocks/transactions']
    apps = apps + [directory for directory in os.listdir(path) if directory.find('__')]

    if clear_migrations:
        for app in apps:
            migrations_path = app + '/migrations'
            if os.path.exists(migrations_path):
                shutil.rmtree(migrations_path)

    for app in apps:
        call_command('makemigrations', app.split('/')[-1], interactive=False)

    call_command('migrate')
