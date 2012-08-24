from google.appengine.ext import db
from google.appengine.api import users


class Trader(db.Model):
    name = db.StringProperty(required=True)
    address = db.StringProperty(multiline=True)
    website = db.LinkProperty()
    location = db.GeoPtProperty()
    favorite = db.BooleanProperty(default=False)

    created_by = db.UserProperty(required=True, auto_current_user=True)
    created_on = db.DateTimeProperty(auto_now_add=True)
    modified_on = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(required=True, auto_current_user=True)


class Contact(db.Model):
    name = db.StringProperty(required=True)
    email = db.StringProperty()
    type = db.StringProperty()
    phone = db.StringProperty()
    role = db.StringProperty()
    trader = db.ReferenceProperty(Trader, collection_name='contacts')
    
    created_by = db.UserProperty(required=True, auto_current_user=True)
    created_on = db.DateTimeProperty(auto_now_add=True)
    modified_on = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.UserProperty(required=True, auto_current_user=True)