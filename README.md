# Docshare
This project creates an interface for sharing files.
It also allows user to create folder and upload files and do various other operations like list files, download and delete files. 

## Getting Started
Create a file local_settings.py in the same folder as settings.py file having your database details as
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'docshare',
            'USERNAME': 'username',
            "PASSWORD": 'password'
        }
    }

### Prerequisites

Python 3.6
Django 2.0

