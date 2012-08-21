import logging
import webapp2
from model import Trader
from google.appengine.ext import db
from google.appengine.api import users
import os
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class TraderPage(webapp2.RequestHandler):
    def get(self,*kwargs):

        traders_query = Trader.all().order('-created_on')
        traders = traders_query.fetch(10)

        if len(traders) == 0:
            logging.info('No traders assign for user %s', users)

        template_values = {
            'traders': traders,
            'logout_url':users.create_logout_url(self.request.uri)
        }

        template = jinja_environment.get_template('trader.html')
        self.response.out.write(template.render(template_values))
        
    def post(self,*kwargs):

        trader = Trader(name=self.request.get('name'))

        trader.address = self.request.get('address')
        trader.website = self.request.get('website')
        trader.location = db.GeoPt(self.request.get('latitude'),self.request.get('longitude'))

        trader.author = users.get_current_user().nickname()

        trader.put()
        self.redirect('/traders/')

class TraderListPage(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>HOLA</body></html>')

