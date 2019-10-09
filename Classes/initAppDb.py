
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class InitAppDb():

    def __init__(self):
        super().__init__()    

    def getAppDb(self):
        app = Flask(__name__)
        app.config.from_object('config')

        db  = SQLAlchemy(app)
        db.app = app
        db.init_app(app)
        return app, db