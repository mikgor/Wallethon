import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
application = get_wsgi_application()

from django.core.management import call_command

os.chdir("..")
path = os.getcwd() + '/apps'

apps = ['main', 'markets', 'transactions']
apps = apps + [directory for directory in os.listdir(path) if os.path.isdir(directory) and directory.find('__')]

for app in apps:
    call_command('makemigrations', app, interactive=False)

call_command('migrate')
