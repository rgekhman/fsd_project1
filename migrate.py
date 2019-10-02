#
# https://www.google.com/search?q=flask+migrate+create+table+columns&rlz=1C1CHBF_enUS820US820&oq=flask+migrate+create+table+columns&aqs=chrome..69i57.18237j0j7&sourceid=chrome&ie=UTF-8#kpvalbx=_r6qUXda8Ne2FggeK-KuwCg24
#
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)
print(migrate)
