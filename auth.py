import webapp2
import jinja2
import os
from django.utils import simplejson
from webapp2_extras import auth
from webapp2_extras import sessions
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
import logging


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def user_required(handler):
    """
         Decorator for checking if there's a user associated with the current session.
         Will also fail if there's no session present.
     """
    def check_login(self, *args, **kwargs):
        auth = self.auth

        if not auth.get_user_by_session():
            # If handler has no login_url specified invoke a 403 error
            logging.info("Checking is not logged")
            try:
                self.redirect(self.auth_config['login_url'], abort=True)
            except (AttributeError, KeyError), e:
                self.abort(403)
        else:
            logging.info("Checking is login")
            return handler(self, *args, **kwargs)

    return check_login


class BaseHandler(webapp2.RequestHandler):
    """
         BaseHandler for all requests

         Holds the auth and session properties so they are reachable for all requests
     """

    def save(self,model):

        user_id=self.auth.get_user_by_session()['user_id']
        model.created_by=user_id
        model.modified_by=user_id
        model.put()

    def dispatch(self):
        try:
            response = super(BaseHandler, self).dispatch()
            #self.response.write(response)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def session_store(self):
        return sessions.get_store(request=self.request)

    @webapp2.cached_property
    def auth_config(self):
        """
              Dict to hold urls for login/logout
          """
        return {
            'login_url': self.uri_for('login'),
            'logout_url': self.uri_for('logout')
        }


class LoginHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('templates/login.html')
        self.response.out.write(template.render({}))

    def post(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if self.login(username,password):
            self.redirect('/')
        else:
            self.redirect('/login/')

    def login(self, username, password):
        try:
            self.auth.get_user_by_password(username, password)
            return True
        except (InvalidAuthIdError, InvalidPasswordError), e:
            # Returns error message to self.response.write in the BaseHandler.dispatcher
            # Currently no message is attached to the exceptions
            return False


class JsonLoginHandler(LoginHandler):
    def post(self):
        try:
            json_request= simplejson.loads(self.request.body)
            #TODO: return profile
            if self.login(json_request['username'],json_request['password']):
                return simplejson.dumps({'success':True,'message':'Login Successful'})


            #TODO: better error message
            return simplejson.dumps({'success':False,'message':'Error in login for %s' % json_request['username']})

        except ValueError as e:
            #TODO: improve error message
            return simplejson.dumps({'success':False,'message':'Unparseable JSON string'})




class CreateUserHandler(BaseHandler):
    def get(self):
        template = jinja_environment.get_template('templates/create_user.html')
        self.response.out.write(template.render({}))

    @user_required
    def post(self):
        """
              username: Get the username from POST dict
              password: Get the password from POST dict
          """
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        # Passing password_raw=password so password will be hashed
        # Returns a tuple, where first value is BOOL. If True ok, If False no new user is created
        user = self.auth.store.user_model.create_user(username, password_raw=password)
        if not user[0]: #user is a tuple
            return user[1] # Error message
        else:
            # User is created, let's try redirecting to login page
            try:
                self.redirect(self.auth_config['login_url'], abort=True)
            except (AttributeError, KeyError), e:
                self.abort(403)


class LogoutHandler(BaseHandler):
    """
         Destroy user session and redirect to login
     """

    def get(self):
        self.auth.unset_session()
        # User is logged out, let's try redirecting to login page
        try:
            self.redirect(self.auth_config['login_url'])
        except (AttributeError, KeyError), e:
            return "User is logged out"