import webapp2
from trader import *
from contact import *
from auth import  *
from google.appengine.ext import db
from google.appengine.api import users
import os
import logging
import jinja2


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainPage(BaseHandler):
    @user_required
    def get(self):
        template = jinja_environment.get_template('templates/index.html')
        self.response.out.write(template.render())


#TODO: Make the request through a UID instead of a int to get any image we want/or need
class GetImage(webapp2.RequestHandler):
    def get(self,image_id):
        trader= Trader.get_by_id(int(image_id))
        if trader.logo:
            self.response.headers['Content-Type'] = 'image/png'
            self.response.out.write(trader.logo)
        else:
            self.response.out.write('No Image Found')


logging.getLogger().setLevel(logging.DEBUG)

config  = {}
config['webapp2_extras.sessions'] = {
    'secret_key': '208e12f0faab5d7c633b3978e04bc5f2'
}



app = webapp2.WSGIApplication([
    ('/',MainPage),
    ('/traders[/]*', TraderListPage),
    ('/traders/add', TraderPage),
    ('/contact/(\d+)[/]*', ContactListPage),
    ('/contact/(\d+)/add[/]*', ContactPage),
    ('/json/contact/(\d+)/add[/]*', ContactJsonPage),
    ('/json/traders/(.*)', JsonTraderPage),
    (r'/json/login/', JsonLoginHandler),
    webapp2.Route(r'/images/<image_id:\d+>', handler=GetImage),
    #Custom Authentication
    webapp2.Route(r'/login/', handler=LoginHandler, name='login'),
	webapp2.Route(r'/logout/', handler=LogoutHandler, name='logout'),
	webapp2.Route(r'/create/', handler=CreateUserHandler, name='create-user'),],
                                         debug=True,config=config)





