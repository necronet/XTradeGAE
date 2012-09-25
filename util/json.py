import datetime
from datastore.model import Trader,Contact
from google.appengine.api import users
from google.appengine.ext import db
from django.utils import simplejson
import settings

class jsonEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()

        elif isinstance(obj, db.Model):
            data=dict((p, getattr(obj, p))
                        for p in obj.properties())
            if isinstance(obj, Trader):
                data['contacts']= obj.contacts()
                data['logo'] =settings.IMAGE_URL%obj.key().id()
            if isinstance(obj, Contact):
                del data['trader']

            return data

        elif isinstance(obj, db.GeoPt):
            return {'lat': obj.lat, 'lon': obj.lon}

        elif isinstance(obj, users.User):
            return obj.email()

        else:
            return simplejson.JSONEncoder.default(self, obj)

def encode(data):
    return simplejson.dumps(data, cls=jsonEncoder)