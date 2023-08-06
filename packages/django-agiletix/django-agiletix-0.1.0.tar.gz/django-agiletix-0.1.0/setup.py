from distutils.core import setup
setup(
  name = 'django-agiletix',
  packages = ['agiletix'],
  version = '0.1.0',
  description = 'A Django app for interacting with the Agile Ticketing API',
  author = 'Gene Sluder',
  author_email = 'gene@gobiko.com',
  url = 'https://github.com/genesluder/django-agiletix',
  download_url = 'https://github.com/genesluder/django-agiletix/tarball/0.1.0',
  keywords = [
    'agile', 
    'agiletix',
    'agile ticketing',  
    'django'
  ],
  classifiers = [],
  install_requires=[
    'agiletixapi',
    'celery',
  ],
)
