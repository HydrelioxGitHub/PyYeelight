from distutils.core import setup
setup(
  name = 'pyyeelight',
  packages = ['pyyeelight'], # this must be the same as the name above
  install_requires = ['voluptuous'],
  version = '1.0-beta',
  description = 'a simple python3 library for Yeelight Wifi Bulbs',
  author = 'Hydreliox',
  author_email = 'hydreliox@gmail.com',
  url = 'https://github.com/HydrelioxGitHub/pyyeelight', # use the URL to the github repo
  download_url = 'https://github.com/HydrelioxGitHub/pyyeelight/tarball/1.0-beta',
  keywords = ['xiaomi', 'bulb', 'yeelight', 'API'], # arbitrary keywords
  classifiers = [],
)