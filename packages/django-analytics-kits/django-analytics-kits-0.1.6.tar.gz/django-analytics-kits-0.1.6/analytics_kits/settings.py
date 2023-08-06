from __future__ import unicode_literals

from django.conf import settings

# Number of result to fetch from google analytics for most popular contents
SECRET_KEY = getattr(
    settings, 'ANALYTICS_KIT_SECRET_KEY', settings.SECRET_KEY)
