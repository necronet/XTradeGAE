from django.utils import simplejson
import webapp2
import jinja2
import os
from auth import BaseHandler, user_required
from datastore.model import Trader,Contact

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class ContactListPage(BaseHandler):
    @user_required
    def get(self,trader_id):

        trader=Trader.get_by_id(int(trader_id))

        template_values = {
            'contacts':trader.contacts(),
            'add_link':('%s/add/'% trader_id)
        }

        template = jinja_environment.get_template('templates/contact_list.html')
        self.response.out.write(template.render(template_values))


class ContactPage(BaseHandler):
    @user_required
    def get(self,trader_id):
        template = jinja_environment.get_template('templates/contact.html')
        self.response.out.write(template.render())

    @user_required
    def post(self,trader_id):

        #load the trader reference to be set
        first_name = self.request.get('first_name')
        last_name = self.request.get('last_name')

        trader_reference=Trader.get_by_id(int(trader_id))

        contact = Contact(trader=trader_reference,first_name=first_name,last_name=last_name)

        contact.role = self.request.get('role')
        contact.phone = self.request.get('phone')
        contact.email = self.request.get('email')
    
        self.save(contact)
        
        self.redirect('/contact/%s/' % trader_id)

class ContactJsonPage(BaseHandler):
    @user_required
    def post(self,trader_id):
        contact_json= simplejson.loads(self.request.body)
        trader_reference=Trader.get_by_id(int(trader_id))

        contact = Contact(trader=trader_reference,first_name=contact_json.first_name,last_name=contact_json.last_name)

        contact.role = contact_json.role
        contact.phone = contact_json.phone
        contact.email = contact_json.email
        self.save(contact)

        