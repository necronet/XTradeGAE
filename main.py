import logging
import urllib
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

        traders_query = Trader.all().order('-created_on')
        traders = traders_query.fetch(10)

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        template_values = {
            'traders': traders,
            'url': url,
            'url_linktext': url_linktext
        }

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))


class Guestbook(webapp2.RequestHandler):
  def post(self):
    # We set the same parent key on the 'Greeting' to ensure each greeting is in
    # the same entity group. Queries across the single entity group will be
    # consistent. However, the write rate to a single entity group should
    # be limited to ~1/second.

    trader = Trader(name=self.request.get('name'))

    trader.address = self.request.get('address')
    trader.website = self.request.get('website')

    if users.get_current_user():
      trader.author = users.get_current_user().nickname()


    
    trader.put()
    self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage),
                               ('/sign', Guestbook)],
                              debug=True)




