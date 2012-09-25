from google.appengine.ext import db
from google.appengine.api import users

class BaseModel(db.Model):
    created_by = db.IntegerProperty()
    created_on = db.DateTimeProperty(auto_now_add=True)
    modified_on = db.DateTimeProperty(auto_now_add=True)
    modified_by = db.IntegerProperty()

class Trader(BaseModel):
    name = db.StringProperty(required=True)
    address = db.StringProperty(multiline=True)
    website = db.LinkProperty()
    location = db.GeoPtProperty()
    favorite = db.BooleanProperty(default=False)
    logo = db.BlobProperty()

    def contacts(self):
       return self.contact_set.fetch(50)

class Contact(BaseModel):
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)
    email = db.EmailProperty()
    type = db.StringProperty()
    phone = db.PhoneNumberProperty()
    role = db.StringProperty()
    trader = db.ReferenceProperty(Trader)
