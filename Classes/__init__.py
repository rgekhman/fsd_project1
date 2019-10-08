#from flask_script import Manager
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class initAppDb():

    def getAppDb(self):
        app = Flask(__name__)
        app.config.from_object('config')

        db  = SQLAlchemy(app)
        db.app = app
        db.init_app(app)
        return app, db

i = initAppDb()
app, db = i.getAppDb()

class Venue(db.Model):
    __tablename__ = 'Venue'
    
    # if _db is not None:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String)
    address = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String)


class Artist(db.Model):
   __tablename__ = 'Artist'

   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String)
   city = db.Column(db.String(120))
   state = db.Column(db.String(120))
   address = db.Column(db.String(120))
   phone = db.Column(db.String(120))
   genres = db.Column(db.String)
   image_link = db.Column(db.String)
   facebook_link = db.Column(db.String)
   website = db.Column(db.String)
   seeking_venue = db.Column(db.Boolean)
   seeking_description = db.Column(db.String(500))

class Show(db.Model):
   __tablename__ = 'Show'

   id = db.Column(db.Integer, primary_key=True)
   start_time = db.Column(db.DateTime())
   id = db.Column(db.Integer, primary_key=True)
   start_time = db.Column(db.DateTime())
   venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
   venue = db.relationship('Venue', backref=db.backref('shows', cascade='all, delete'))
   artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
   artist = db.relationship('Artist', backref=db.backref('shows', cascade='all, delete'))

db.create_all()