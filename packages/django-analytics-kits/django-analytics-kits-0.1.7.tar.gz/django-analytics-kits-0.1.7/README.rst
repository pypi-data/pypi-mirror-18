=====================
DJANGO ANALYTICS KITS
=====================

Analytics kits is a Django app to get analytics data from Google Analytics and save them in a model.
It can be used for generating models to record information such as most visited pages in a given period.


Quick start
-----------

1. Install the package::

    # For Ubuntu it requires libffi-dev to be installed on the system.
    # sudo apt-get install libffi-dev

    pip install django-analytics-kits

2. Add "analytics_kits" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'analytics_kits',
    ]

3. Run the migration command to create account model::
    
    python manage.py migrate

4. Define your Google Analytics API service account and private_key in the Django admin section of the Analytics Kits.
   
   If you want to know more about how to generate a private_key and a google service account you can have a look into this link: https://developers.google.com/identity/protocols/OAuth2ServiceAccount
   This service account should have read access to the google analytic view you want to get the information for.

5. Create a model in your app to record the analytics results. This model should be inherited from `analytics_kits.models.AnalyticsResult`::
    
    from analytics_kits.models import AnalyticsResult

    class MostPopular(AnalyticsResult):
        pass


6. Use `analytics_kits.models.AnalyiticsKitsMixin` Mixin for every content type you want get the analytics results for::

    from django.db import models
    from analytics_kits.models import AnalyiticsKitsMixin

    class Article(models.Model, AnalyiticsKitsMixin):
        # model fields
        ...

        # get_absolute_url method should be defined for this model



7. set a Cron job for the management commands `analytics_results` to connect to google analytics API and update your app model::

    python manage.py analytics_results --app YOUR_APP_NAME --model YOUR_MODEL_NAME --view VIEW_ID --account ACCOUNT_NAME

    # YOUR_APP_NAME: Name of the application that you created your content models inside
    # YOUR_MODEL_NAME: Name of the inherited model from `AnalyticsResult`
    # VIEW_ID: Google Analytics View ID
    # ACCOUNT_NAME: The name you defined for the account on the django admin
