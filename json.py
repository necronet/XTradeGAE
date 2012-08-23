import datetime
from google.appengine.api import users
from google.appengine.ext import db
from django.utils import simplejson

class jsonEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        elif isinstance(obj, db.Model):
            return dict((p, getattr(obj, p)) 
                        for p in obj.properties())

        elif isinstance(obj, db.GeoPt):
            return simplejson.dumps({'lat': obj.lat, 'lon': obj.lon})

        elif isinstance(obj, users.User):
            return obj.email()

        else:
            return simplejson.JSONEncoder.default(self, obj)

def encode(data):
    return simplejson.dumps(data, cls=jsonEncoder)