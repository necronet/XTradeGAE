import logging
import webapp2
from datastore.model import Trader
from util import json
from google.appengine.ext import db
from google.appengine.api import users
import os
from auth import BaseHandler, user_required
import jinja2

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class TraderPage(BaseHandler):
    @user_required
    def get(self,*kwargs):

        template_values = {
            'logout_url':users.create_logout_url(self.request.uri)
        }

        template = jinja_environment.get_template('templates/trader.html')
        self.response.out.write(template.render(template_values))

    @user_required
    def post(self,*kwargs):

        trader = Trader(name=self.request.get('name'))

        image = self.request.get('logo')
        trader.logo = db.Blob(image)
        trader.address = self.request.get('address')
        trader.website = self.request.get('website')
        trader.location = db.GeoPt(self.request.get('latitude'),self.request.get('longitude'))

        logging.info("Trader is being add")

        self.save(trader)


        self.redirect('/traders/')

class JsonTraderPage(BaseHandler):
    @user_required
    def get(self, *kwargs):

        traders_query = Trader.all().order('-created_on')
        traders = traders_query.fetch(50)

        data = json.encode(traders)

        self.response.headers['Content-Type'] = 'application/json; charset=utf-8'
        self.response.out.write(data)



class TraderListPage(BaseHandler):
    @user_required
    def get(self):

        traders_query = Trader.all().order('-created_on')
        traders = traders_query.fetch(10)
        
        if len(traders) == 0:
            logger.info('No traders assign for user %s', users)
            

        template_values={
                'traders':traders
        }

        template= jinja_environment.get_template('templates/trader_list.html')

        self.response.out.write(template.render(template_values))

