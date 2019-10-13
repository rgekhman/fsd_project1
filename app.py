#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import os
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy_utils import create_database, database_exists, get_referencing_foreign_keys
import config
from models import db, Artist, Venue, Show
import traceback
from sqlalchemy.orm.exc import NoResultFound



#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
moment = Moment(app)
db.init_app(app)


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500
if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


class CannotRemoveObject(Exception):
    status_code = 521   # custom error code - could not remove item

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')

#region  Venues
@app.route('/venues')
def venues():
    unique_city_states = Venue.query.distinct(Venue.city, Venue.state).all()
    data = [ucs.filter_on_city_state for ucs in unique_city_states]
    #print(data)   
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    search_term = request.form.get('search_term', None)
    venues = Venue.query.filter(
        Venue.name.ilike("%{}%".format(search_term))).all()
    count_venues = len(venues)
    response = {
        "count": count_venues,
        "data": [v.serialize for v in venues]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    venues = Venue.query.filter(Venue.id == venue_id).one_or_none()

    if venues is None:
        Flask.abort(404)

    data = venues.serialize_with_shows_details
    return render_template('pages/show_venue.html', venue=data)

#serve empty form
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    venue_form = VenueForm(request.form)

    try:
        new_venue = Venue(
            name=venue_form.name.data,
            genres=','.join(venue_form.genres.data),
            address=venue_form.address.data,
            city=venue_form.city.data,
            state=venue_form.state.data,
            phone=venue_form.phone.data,
            facebook_link=venue_form.facebook_link.data,
            image_link=venue_form.image_link.data)
        if not new_venue.isExists():
            new_venue.add()
            # on successful db insert, flash success
            flash('Venue ' +
                  request.form['name'] +
                  ' was successfully listed!')
        else:
            flash(  'Venue with a Name: {} , City: {} , and State: {} already exists! New record not inserted'.\
                    format(request.form['name'], request.form['city'], request.form['state']))
    except Exception as ex:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be listed.')
        traceback.print_exc()

    return render_template('pages/home.html')

@app.route('/venues/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue(id = venue_id)
    try:
        isVenueExistsInShows, shows = venue.isVenueExistsInShows()
        if not isVenueExistsInShows:
            venue.delete()

            response = jsonify(type="success")
            response.status_code = 200
            return response
        else: 
            raise CannotRemoveObject('Cannot remove this venue because it is used in {} Shows'.format(len(shows)))
    
    except CannotRemoveObject as ex:
        _message = 'Venue could not be deleted. ' + ex.message
        response = jsonify(type="error", message=_message)
        response.status_code = ex.status_code
        return response

    except Exception as ex:
        _message = 'An error occurred. ' + ex.args[0]
        response = jsonify(type="error", message=_message)
        response.status_code = 522 #custom server error code
        return response       

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue_form = VenueForm()

    venue_to_update = Venue.query.filter(Venue.id == venue_id).one_or_none()
    if venue_to_update is None:
        Flask.abort(404)

    venue = venue_to_update.serialize
    form = VenueForm(data=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):  
    form = VenueForm(request.form)
    try:
        venue = Venue.query.filter(Venue.id==venue_id).one()
        venue.name = form.name.data,
        venue.address = form.address.data,
        venue.genres = '.'.join(form.genres.data),  # array json
        venue.city = form.city.data,
        venue.state = form.state.data,
        venue.phone = form.phone.data,
        venue.facebook_link = form.facebook_link.data,
        venue.image_link = form.image_link.data,
        venue.update()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash('An error occurred. Venue ' +
              request.form['name'] + ' could not be updated.')

    return redirect(url_for('show_venue', venue_id=venue_id))
#endregion

#region Artists
@app.route('/artists')
def artists():
    artists = Artist.query.all()
    data = [artist.serialize_with_shows_details for artist in artists]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', None)
    artists = Artist.query.filter(
        Artist.name.ilike("%{}%".format(search_term))).all()
    count_artists = len(artists)
    response = {
        "count": count_artists,
        "data": [a.serialize for a in artists]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    artist = Artist(id = artist_id)    
    try:
        isArtistExistsInShows, shows = artist.isArtistExistsInShows()
        if not isArtistExistsInShows:
            artist.delete()
            response = jsonify(type="success")
            response.status_code = 200
            return response
        else: 
            raise CannotRemoveObject('Cannot remove this artist because it is used in {} Shows'.format(len(shows)))

    except CannotRemoveObject as ex:
        _message = 'Artist could not be deleted. ' + ex.message
        response = jsonify(type="error", message=_message)
        response.status_code = ex.status_code
        return response 

    except Exception as ex:
        _message = 'An error occurred. ' + ex.args[0]
        response = jsonify(type="error", message=_message)
        response.status_code = 522 #custom server error code
        return response       


@app.route('/artists/<int:artist_id>', methods=['POST','GET'])
def show_artist(artist_id):
    artist = Artist.query.filter(Artist.id == artist_id).one_or_none()
    if artist is None:
        flash('Artist could not be found.')

    data = artist.serialize_with_shows_details
    return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist_form = ArtistForm()

    artist_to_update = Artist.query.filter(
        Artist.id == artist_id).one_or_none()
    if artist_to_update is None:
        Flask.abort(404)

    artist = artist_to_update.serialize
    form = ArtistForm(data=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    form = ArtistForm(request.form)
    try:
        artist = Artist.query.filter_by(id=artist_id).one()
        artist.name = form.name.data,
        artist.genres = json.dumps(form.genres.data),  # array json
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.facebook_link = form.facebook_link.data,
        artist.image_link = form.image_link.data,
        artist.update()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully updated!')
    except Exception as e:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be updated.')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    artist_form = ArtistForm(request.form)

    try:
        new_artist = Artist(
            name=artist_form.name.data,
            genres=','.join(artist_form.genres.data),
            city=artist_form.city.data,
            state=artist_form.state.data,
            phone=artist_form.phone.data,
            facebook_link=artist_form.facebook_link.data,
            image_link=artist_form.image_link.data)

        if not new_artist.isExists():
            new_artist.add()
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
        else:
            flash('Artist with a Name: {} , City: {} , and State: {} already exists! New record not inserted'.\
                    format(request.form['name'], request.form['city'], request.form['state']))

    except Exception as ex:
        flash('An error occurred. Artist ' +
              request.form['name'] + ' could not be listed.')

    return render_template('pages/home.html')
#endregion

#region  Shows
@app.route('/shows')
def shows():
    shows = Show.query.all()
    data = [show.serialize_with_artist_venue for show in shows]
    #print(data)
    return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    show_form = ShowForm(request.form)
    try:
        show = Show(
            artist_id=show_form.artist_id.data,
            venue_id=show_form.venue_id.data,
            start_time=show_form.start_time.data
        )
        
        if show.start_time is None:
            flash('Show could not be listed. Please make sure that a Show Start Time is in a format YYYY-MM-DD HH:MM:SS.')
            return render_template('pages/home.html')

        if not show.isExists():
            show.add()
            flash('Show was successfully listed!')
        else:
            flash('Show for this artist / venue / time already exists!')
    except Exception as e:
        flash('An error occurred. Show could not be listed.')

    return render_template('pages/home.html')

@app.route('/shows/<int:show_id>', methods=['DELETE'])
def delete_show(show_id):
    show = Show(id = show_id)
    try:
        show.delete()
        response = jsonify(type="success")
        response.status_code = 200
        return response

    except Exception as ex:
        _message = 'An error occurred. ' + ex.args[0]
        response = jsonify(type="error", message=_message)
        response.status_code = 522 #custom server error code
        return response    


#endregion " Shows " 

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)
