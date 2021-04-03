import os

from scripts.make_migrations import make_migrations
from scripts.populate_db import populate_db


os.chdir("..")

db_path = os.getcwd() + "/db.sqlite3"

if os.path.exists(db_path):
    print('Removing db...')
    os.remove(db_path)

print('Making migrations...')
make_migrations(clear_migrations=True)

print('Populating db...')
populate_db()
