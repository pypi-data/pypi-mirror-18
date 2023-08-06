import logging

import browserid
import cherrypy


def require_signin(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'persona.require' not in f._cp_config:
            f._cp_config['persona.require'] = []
        f._cp_config['persona.require'].extend(conditions)
        return f
    return decorate


def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.session.get('username', None)


def any_of(*conditions):
    """Returns True if any of the conditions match"""
    def check():
        for c in conditions:
            if c():
                return True
        return False
    return check


# By default all conditions are required, but this might still be
# needed if you want to use it inside of an any_of(...) condition
def all_of(*conditions):
    """Returns True if all of the conditions match"""
    def check():
        for c in conditions:
            if not c():
                return False
        return True
    return check


class PersonaListener(object):

    def login(self):
        pass

    def logout(self):
        pass


class Persona(cherrypy.Tool):

    def __init__(self, env, audience="HOST"):
        """
        When initialized, the tool installs itself into the 'before_handler'
        hook at the default priority.

        As a result, for every request for which the tool is enabled,
        self.authenticate will be invoked.
        """
        super(Persona, self).__init__('before_handler', self.authenticate)
        self.env = env
        self.audience = audience
        self._listeners = []

    def authenticate(self, login_path='/login', logout_path='/logout', require=None):
        """
        Entry point for this tool.

        Audience is the host name and port on which this server is hosting.
        It may be set to 'HOST' to use the HOST header, but this setting
        SHOULD ONLY BE USED when the HOST header has been verified by a
        trusted party (such as a reverse-proxy).
        """

        if cherrypy.request.path_info == login_path:
            cherrypy.request.handler = self.login
            return
        elif cherrypy.request.path_info == logout_path:
            cherrypy.request.handler = self.logout
            return

        if require is not None and not cherrypy.session.get('username', None):
            raise cherrypy.HTTPRedirect(require + '?file=' + cherrypy.request.path_info)

        conditions = cherrypy.request.config.get('persona.require', None)

        if conditions is not None:

            if self.audience == 'HOST':
                self.audience = cherrypy.request.headers['HOST']

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
        return self.env.get_template('login.html').render()

    def login(self):
        cherrypy.response.headers['Cache-Control'] = 'no-cache'

        assertion = cherrypy.request.params['assertion']
        # Verify the assertion using browserid.
        validation = browserid.verify(assertion, self.audience)

        # Check if the assertion was valid
        if validation['status'] != 'okay':
            raise cherrypy.HTTPError(400, "invalid")

        # Log the user in by setting the username
        cherrypy.session['username'] = validation['email']

        for listener in self._listeners:
            try:
                listener.login()
            except Exception as e:
                logging.error("Persona listener: {}".format(e))

        return 'You are logged in'

    def logout(self):
        cherrypy.response.headers['Cache-Control'] = 'no-cache'

        if 'username' in cherrypy.session:
            del cherrypy.session['username']

        for listener in self._listeners:
            try:
                listener.logout()
            except Exception as e:
                logging.error("Persona listener: {}".format(e))

        return self.env.get_template('logout.html').render()

    def add_listener(self, listener: PersonaListener):
        self._listeners.append(listener)

    def remove_listener(self, listener: PersonaListener):
        self._listeners.remove(listener)