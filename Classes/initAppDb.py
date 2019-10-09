
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class CInitAppDb():

    def getAppDb(self):
        app = Flask(__name__)
        app.config.from_object('config')

        db  = SQLAlchemy(app)
        db.app = app
        db.init_app(app)
        return app, db