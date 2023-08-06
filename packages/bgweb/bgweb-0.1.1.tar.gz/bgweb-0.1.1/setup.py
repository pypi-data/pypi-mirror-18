from distutils.core import setup
from setuptools import find_packages

VERSION = "0.1.1"
AUTHORS = "Barcelona Biomedical Genomics Lab"
CONTACT_EMAIL = "bbglab@irbbarcelona.org"

setup(
    name="bgweb",
    version=VERSION,
    packages=find_packages(),
    author=AUTHORS,
    author_email=CONTACT_EMAIL,
    description="BBGLab web framework",
    url="https://bitbucket.org/bgframework/bgweb",
    install_requires=['cherrypy', 'PyMongo', 'PyBrowserid', 'jinja2', 'configobj', 'requests']
)
