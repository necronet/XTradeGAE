from google.appengine.ext import db
from google.appengine.api import users


class Trader(db.Model):

  name = db.StringProperty(required=True)
  address = db.StringProperty(multiline=True)
  website = db.LinkProperty()
  location = db.GeoPtProperty()
  created_by = db.UserProperty(required=True,auto_current_user=True)
  created_on = db.DateTimeProperty(auto_now_add=True)
  modified_on = db.DateTimeProperty(auto_now_add=True)
  modified_by = db.UserProperty(required=True,auto_current_user=True)


class Contact(db.Model):
    pass