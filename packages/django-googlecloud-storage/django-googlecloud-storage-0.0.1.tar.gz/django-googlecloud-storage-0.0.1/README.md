django-googlecloud-storage
===========================

Google Cloud Storage file backend for Django

Based on an django-google-cloud-storage but now made simpler because it uses the python
google-cloud package.

If you run your projects on Google's appengine and you are using the django framework you might need this
file backend since there is no way to upload files, images, etc on appengine. The other solution is using
django-storages and apache libcloud but that soon descended into a debugging rabbit hole.


Prerequisites
-------------

This version works with the google-cloud package from google. It is listed as a dependency.


Installation
-------------

    pip install django-googlecloud-storage


Configuration
-------------

On your django settings.py file you need to add the following settings:

    GOOGLE_CLOUD_STORAGE_PROJECT = '<name-of-project>'
    GOOGLE_CLOUD_STORAGE_BUCKET = '<name-of-bucket>'
    DEFAULT_FILE_STORAGE = 'django.googlecloud.storage.GoogleCloudStorage'
    MEDIA_URL = "https://storage.googleapis.com/<name-of-bucket>/"



Credits
-------

In historical order:

    Christos Kopanos (@ckopanos) - original work using an older version of the google client libs 
    Richard Caceres (@rchrd2) - packaged the original into python module
    Suresh V(@sureshvv) - used the new google-cloud package and namespace packages
