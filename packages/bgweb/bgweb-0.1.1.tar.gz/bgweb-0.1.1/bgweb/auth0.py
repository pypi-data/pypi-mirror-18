import json
import os
import logging
from functools import wraps
import cherrypy
import requests


def require_signin(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'authentication.require' not in f._cp_config:
            f._cp_config['authentication.require'] = []
        f._cp_config['authentication.require'].extend(conditions)
        return f
    return decorate


def auth_redirect(redirect_page):
    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if cherrypy.session.get('username', None) is None:
                # Redirect to Login page here
                raise cherrypy.HTTPRedirect(redirect_page)
            return f(*args, **kwargs)

        return decorated
    return requires_auth

class AuthListener:

    def login(self):
        pass

    def logout(self):
        pass


class RegisteredUserListener(AuthListener):

    def __init__(self, registered_file):
        self.register_file = registered_file
        if os.path.isfile(registered_file):
            self.registered_users = [u.strip().lower() for u in open(registered_file)]
        else:
            open(registered_file, 'a').close()
            self.registered_users = []

    def login(self):
        user_id = cherrypy.session['username']
        if user_id not in self.registered_users:
            self.register_user(user_id)

    def register_user(self, user):
        with open(self.register_file, 'at') as fd:
            fd.write(user + '\n')
        self.registered_users.append(user)


class AuthenticationTool(cherrypy.Tool):

    def __init__(self, env, callable):
        super(AuthenticationTool, self).__init__('before_handler', callable)
        self.env = env
        self._listeners = []


    def add_listener(self, listener: AuthListener):
        self._listeners.append(listener)

    def remove_listener(self, listener: AuthListener):
        self._listeners.remove(listener)

class Auth0(AuthenticationTool):

    def __init__(self, env):
        super(Auth0, self).__init__(env, self.authenticate)

    def authenticate(self, login_path='/callback', logout_path='/logout', require=None):
        """
        Entry point for this tool.
        """


        if cherrypy.request.path_info == login_path:
            cherrypy.request.handler = self.auth0_callback
            return
        elif cherrypy.request.path_info == logout_path:
            cherrypy.request.handler = self.logout
            return

        if require is not None and not cherrypy.session.get('username', None):
            raise cherrypy.HTTPRedirect(require + '?file=' + cherrypy.request.path_info)

        conditions = cherrypy.request.config.get('authentication.require', None)

        if conditions is not None:

            if not cherrypy.session.get('username', None):
                # the user is not logged in, but the tool is enabled, so instead
                #  of allowing the default handler to run, respond instead with
                #  the authentication page.
                cherrypy.request.handler = self.force_login
            else:
                if conditions is None:
                    conditions = []

                for condition in conditions:
                    # A condition is just a callable that returns true or false
                    if not condition():
                        cherrypy.request.handler = self.force_login


    def force_login(self):
        """
        This handler replaces the default handler when the user is not yet
        authenticated.
        Return a response that will:
         - trigger persona to authenticate the user
         - on success, try to load the page again
        """
        return self.env.get_template('login.html').render(fordward_to=cherrypy.request.path_info)

    def auth0_callback(self):
        code = cherrypy.request.params.get('code', None)
        page = cherrypy.request.params.get('page', None)
        error = cherrypy.request.params.get('error', None)
        error_description = cherrypy.request.params.get('error_description', None)

        if error is not None:
            raise cherrypy.HTTPRedirect(page + '?msg=' + error_description)

        json_header = {'content-type': 'application/json'}

        token_url = "https://{domain}/oauth/token".format(domain=self.env.globals['AUTH0_DOMAIN'])

        token_payload = {
            'client_id': self.env.globals['AUTH0_CLIENT_ID'],
            'client_secret': self.env.globals['AUTH0_CLIENT_SECRET'],
            'redirect_uri': self.env.globals['AUTH0_CALLBACK_URL'],
            'code': code,
            'grant_type': 'authorization_code'
        }

        token_info = requests.post(token_url, data=json.dumps(token_payload), headers=json_header).json()

        user_url = "https://{domain}/userinfo?access_token={access_token}".format(
            domain=self.env.globals['AUTH0_DOMAIN'],
            access_token=token_info[
                'access_token'])

        user_info = requests.get(user_url).json()

        # We're saving all user information into the session
        cherrypy.session['username'] = user_info.get('email')
        # TODO get all the info you want from the user (and put in user_data)

        for listener in self._listeners:
            try:
                listener.login()
            except Exception as e:
                logging.error("Auth0 listener: {}".format(e))

        raise cherrypy.HTTPRedirect(page)


    def logout(self):
        cherrypy.response.headers['Cache-Control'] = 'no-cache'

        if 'username' in cherrypy.session:
            del cherrypy.session['username']

        for listener in self._listeners:
            try:
                listener.logout()
            except Exception as e:
                logging.error("Auth0 listener: {}".format(e))

        raise cherrypy.HTTPRedirect("home?msg='Logged out'")
