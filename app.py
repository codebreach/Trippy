from flask import Flask
import os
import foursquare
import json

app = Flask(__name__)

fb_client_id = "0VKLLPOXT2ZHPSMMO3XNJPVW43G2J1W33HR5SFW3GH0O10S1"
fb_client_secret = "TX5J4PEABTFNUPYB5TS0ED4F2DFRZSLJUGI0NWKBBDUSO3X0"
instagram_client_id = "0790cbf24ff84eb2ab0f57660dacc016"
instagram_client_secret = "055b5b7661564c2197c0b92d1105bbb1"

client = foursquare.Foursquare(client_id=fb_client_id, 
                               client_secret=fb_client_secret, 
                               redirect_uri='http://hidden-inlet-2627.herokuapp.com/callback')

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/place/<location>")
def hello(location):
    app.logger.debug("GOT REQUEST FOR " + location)
    output = json.dumps(get_4sq_place(location))
    return output

@app.route("/instagram/callback")
def instagram_callback():
    return "asd"

def get_4sq_place(location):
    return client.venues.search(params={'near':location})

if __name__ == "__main__":
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
