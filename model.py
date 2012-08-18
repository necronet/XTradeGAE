from google.appengine.ext import db
from google.appengine.api import users


class Trader(db.Model):

  name = db.StringProperty()
  address = db.StringProperty(multiline=True)
  location = db.GeoPtProperty()
  website = db.LinkProperty()
  author = db.StringProperty()
  created_on = db.DateTimeProperty(auto_now_add=True)
  modified_on = db.DateTimeProperty(auto_now_add=True)
