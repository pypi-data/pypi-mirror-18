from distutils.core import setup
setup(
  name = 'agiletixapi',
  packages = ['agiletixapi'],
  version = '0.1.0',
  description = 'A Python interface for the Agile Ticketing API.',
  author = 'Gene Sluder',
  author_email = 'gene@gobiko.com',
  url = 'https://github.com/genesluder/python-agiletixapi',
  download_url = 'https://github.com/genesluder/python-agiletixapi/tarball/0.1.0',
  keywords = [
    'agile', 
    'agiletix',
    'agile ticketing',  
  ],
  classifiers = [],
  install_requires=[
    'jsonobject',
    'slumber',
    'pytz',
  ],
)
