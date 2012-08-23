import webapp2
from trader import TraderPage,TraderListPage,JsonTraderPage
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

app = webapp2.WSGIApplication([
    (r'/',MainPage),
    (r'/traders/', TraderListPage),
    (r'/traders/add', TraderPage),
    (r'/json/traders/(.*)', JsonTraderPage)],
                                         debug=True)





