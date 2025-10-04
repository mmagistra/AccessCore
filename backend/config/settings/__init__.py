import os

environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .prod import *
else:
    from .dev import *