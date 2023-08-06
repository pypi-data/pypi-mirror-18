from bgweb.auth0 import Auth0, RegisteredUserListener
from configobj import ConfigObj
from validate import Validator

from bgweb.apps.bgwebapp import BGWebApp
import cherrypy
from jinja2 import Environment


class BGWeb:

    def __init__(self, sessions=True, auth=True, gzip=True, root="/"):
        self.sessions = sessions
        self.auth = auth
        self.gzip = gzip
        self.root = root

    def run(self,
            conf: ConfigObj,
            webapp: BGWebApp,
            static_dirs: dict,
            environment: Environment,
            auth_listeners: list = [],
            global_vars: dict = {},
            userdata_dir=None):


        if self.auth:
            auth = ConfigObj('../conf/auth0.conf', configspec='../conf/auth0.confspec')
            auth.validate(Validator())
            for k, v in auth.items():
                environment.globals[k] = v
            cherrypy.tools.authentication = Auth0(environment)
            for l in auth_listeners:
                cherrypy.tools.authentication.add_listener(l)
            if 'users_file' in conf['website']:
                cherrypy.tools.authentication.add_listener(RegisteredUserListener(conf['website']['users_file']))

        server_conf = {
            self.root: {
                'tools.sessions.on': self.sessions,
                'tools.authentication.on': self.auth,
                'tools.gzip.on': self.gzip
            }
        }
        for static_dir, value in static_dirs.items():
            if type(value) == dict:
                server_conf[static_dir] = value
            elif type(value) == str:
                server_conf[static_dir] = {
                    'tools.staticdir.on': True,
                    'tools.staticdir.dir': value
                }

        server_conf['userdata'] = {'dir': userdata_dir}
        for k, v in global_vars.items():
            if k not in server_conf:
                server_conf[k] = v
            else:
                raise RuntimeError("Global variable '{}' trying to mask static dir or other server conf".format(k))

        cherrypy.tree.mount(webapp, self.root, server_conf)
        cherrypy.config.update({'server.socket_port': int(conf['website']['port'])})
        cherrypy.engine.start()
        cherrypy.engine.block()



if __name__ == '__main__':
    NotImplementedError("This class should be extended and run from a user class")