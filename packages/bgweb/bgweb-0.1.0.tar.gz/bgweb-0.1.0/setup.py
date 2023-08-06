from distutils.core import setup
from setuptools import find_packages
from bgweb import VERSION, AUTHORS, CONTACT_EMAIL

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
