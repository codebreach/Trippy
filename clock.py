import foursquare
import json
import pymongo
from datetime import datetime
from pymongo import Connection
from apscheduler.scheduler import Scheduler
fb_client_id = "0VKLLPOXT2ZHPSMMO3XNJPVW43G2J1W33HR5SFW3GH0O10S1"
fb_client_secret = "TX5J4PEABTFNUPYB5TS0ED4F2DFRZSLJUGI0NWKBBDUSO3X0"

sched = Scheduler()
mongo_config = "mongodb://heroku_app8040801:ng7kdd6lg3jr9bos8fjrabu91f@ds037987.mongolab.com:37987/heroku_app8040801"
# TODO(madhav): get the mongo config from heroku:config

client = foursquare.Foursquare(client_id=fb_client_id, 
                               client_secret=fb_client_secret, 
                               redirect_uri='http://hidden-inlet-2627.herokuapp.com/callback')

db = Connection(host=mongo_config)[u'heroku_app8040801']

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

@sched.interval_schedule(hours=1)
def foursquare_downloader():
    se={'n':40.698611, 'w':73.954167}
    sw={'n':40.696944, 'w':74.023333}
    nw={'n':40.770833, 'w':74.008889}
    ne={'n':40.698611, 'w':73.954167}
    n_jump = (nw['n'] - se['n'])/16
    w_jump = (nw['w'] - se['w'])/8
    for n in drange(se['n'], nw['n'], n_jump):
        for w in drange(se['w'], nw['w'], w_jump):
            query_time = datetime.utcnow()
            print "MAKING QUERY {0},-{1} at {2}ms".format(n,w,query_time)
            places = client.venues.trending(params={'ll':'{0:.6f},-{1:.6f}'.format(n, w), 
                                                    'limit':30,
                                                    'radius':500});
            print "QUERY DONE"
            venues = []
            query_collection = []
            for venue in places['venues']:
                venue['_id'] = venue['id'] #maybe create a copy?
                venues.append(venue)
                query_collection.append({'n':n, 
                                         'w':w, 
                                         'fsq_id':venue['id'], 
                                         'time':query_time,
                                         'hereNow':venue['hereNow']})
                #TODO(mbhagat): check if the id already exists and update it
            if len(venues) == 0:
                continue
            print "GETTING DB"
            search_results = db['trending_cron_results']
            print "INSERTING {0} into trending results".format(len(query_collection))
            search_results.insert(query_collection)
            places_collection = db['foursquare_places']
            print "INSERTING {0} into places".format(len(venues))
            places_collection.insert(venues)
            print "DONE LOOP"

@sched.interval_schedule(minutes=3)
def timed_job():
    print 'This job is run every three minutes.'

@sched.cron_schedule(day_of_week='mon-fri', hour=17)
def scheduled_job():
    print 'This job is run every weekday at 5pm.'

sched.start()

while True:
    pass
    
