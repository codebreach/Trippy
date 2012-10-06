import os
import foursquare
import flask
import json
import pymongo

from functools import wraps
from flask import Flask, request, current_app
from pymongo import Connection

app = Flask(__name__)

fb_client_id = "0VKLLPOXT2ZHPSMMO3XNJPVW43G2J1W33HR5SFW3GH0O10S1"
fb_client_secret = "TX5J4PEABTFNUPYB5TS0ED4F2DFRZSLJUGI0NWKBBDUSO3X0"
instagram_client_id = "0790cbf24ff84eb2ab0f57660dacc016"
instagram_client_secret = "055b5b7661564c2197c0b92d1105bbb1"

mongo_config = "mongodb://heroku_app8040801:ng7kdd6lg3jr9bos8fjrabu91f@ds037987.mongolab.com:37987/heroku_app8040801"
# TODO(madhav): get the mongo config from heroku:config

client = foursquare.Foursquare(client_id=fb_client_id, 
                               client_secret=fb_client_secret, 
                               redirect_uri='http://hidden-inlet-2627.herokuapp.com/callback')

db = Connection(host=mongo_config)[u'heroku_app8040801']

@app.route("/place/<location>")
def get_place(location):
    func = jsonp(place_handler)
    return func(location)

def place_handler(location):
    app.logger.debug("GOT REQUEST FOR " + location)
    output = json.dumps(get_4sq_place(location))
    return {'data' : output}

@app.route("/instagram/callback")
def instagram_callback():
    return "asd"


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = str(func(*args, **kwargs)['data'])
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function

def get_4sq_place(location):
    places = client.venues.search(params={'near':location})
    venues = []
    for venue in places['venues']:
        venue['_id'] = venue['id'] #maybe create a copy?
        venues.append(venue)
        #TODO(mbhagat): check if the id already exists and update it
    places_collection = db['foursquare_places']
    places_collection.insert(venues)
    return places;

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    from werkzeug import SharedDataMiddleware
    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
      '/': os.path.join(os.path.dirname(__file__), 'client/app')
    })
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    
