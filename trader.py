import logging
import webapp2
from model import Trader,Contact
import json
from google.appengine.ext import db
from google.appengine.api import users
import os
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())

class TraderPage(webapp2.RequestHandler):
    def get(self,*kwargs):

        template_values = {
            'logout_url':users.create_logout_url(self.request.uri)
        }

        template = jinja_environment.get_template('templates/trader.html')
        self.response.out.write(template.render(template_values))
        
    def post(self,*kwargs):

        trader = Trader(name=self.request.get('name'))

        trader.address = self.request.get('address')
        trader.website = self.request.get('website')
        trader.location = db.GeoPt(self.request.get('latitude'),self.request.get('longitude'))

        trader.author = users.get_current_user().nickname()

        trader.put()

        #TODO: put real values here
        contact = Contact(name='Example of contact')
        contact.trader=trader
        contact.put()


        self.redirect('/traders/')

class JsonTraderPage(webapp2.RequestHandler):
    def get(self, *kwargs):
        traders_query = Trader.all().order('-created_on')
        traders = traders_query.fetch(10)
        data = json.encode(traders)
        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(data)

class TraderListPage(webapp2.RequestHandler):
    def get(self):

        traders_query = Trader.all().order('-created_on')
        traders = traders_query.fetch(10)
        
        if len(traders) == 0:
            logging.info('No traders assign for user %s', users)
            

        template_values={
                'traders':traders
        }

        template= jinja_environment.get_template('templates/trader_list.html')

        self.response.out.write(template.render(template_values))

