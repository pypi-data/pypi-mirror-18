import os
from .settings import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'pytest.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'driver27',
        'USER': 'postgres',
#        'PASSWORD': '',
#        'PASSWORD': 'mypassword',
        'HOST': '127.0.0.1',
#        'PORT': '5432',
    }
}

LANGUAGE_CODE = 'es'
