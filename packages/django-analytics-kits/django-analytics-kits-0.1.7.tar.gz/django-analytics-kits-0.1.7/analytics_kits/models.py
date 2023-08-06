from __future__ import unicode_literals

from django.db import models
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

import logging


# A model to save absolute URL for each objects.
# It helps to lookup in different models for an object with an specific URL.
class ObjectUrl(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    url = models.TextField()

    def __unicode__(self):
        return self.url


# Mixin Model to record Urls into ObjectUrl
class AnalyiticsKitsMixin(models.Model):

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        super(AnalyiticsKitsMixin, self).save(
                force_insert=force_insert, force_update=force_update,
                using=using, update_fields=update_fields)
        content_type = ContentType.objects.get_for_model(self)
        try:
            url = self.get_absolute_url()
        except:
            logging.error('get_absolute_url method is not defined')
            return False

        obj_url = ObjectUrl.objects.get_or_create(
                content_type=content_type,
                object_id=self.pk,
                defaults={'url': url}
            )
        obj_url[0].url = url
        obj_url[0].save()

    class Meta:
        abstract = True


# Most popular abstract model
class AnalyticsResult(models.Model):
    pulled_date = models.DateTimeField(
        'Date pulled from analytics', null=True, blank=True)
    title = models.TextField()
    item_url = models.CharField(
        max_length=255, null=True, blank=True, unique=True)
    no_of_views = models.IntegerField()
    object_id = models.PositiveIntegerField(
        db_index=True, null=True, blank=True)
    content_type = models.ForeignKey(
        ContentType, verbose_name=_('Content type'),
        related_name="%(app_label)s_%(class)s",
        null=True, blank=True)
    content_object = GenericForeignKey()

    # You can add extra fields on your inherited model to customise it
    # For example you may want to add publish_date and is_published fields
    #
    # publish_date = models.DateTimeField(blank=True, null=True)
    # is_published = models.BooleanField(default=True)

    class Meta:
        abstract = True

    @staticmethod
    def get_metrics():
        return 'ga:pageviews'

    @staticmethod
    def get_dimensions():
        return 'ga:pagePath,ga:pageTitle'

    @staticmethod
    def get_sort():
        return "-ga:pageviews"

    @staticmethod
    def get_results_count():
        return 50

    @staticmethod
    def get_filters():
        return 'ga:pagePath!~^/$;ga:pagePath!~^/search/*;ga:pagePath!~^/accounts*;ga:pagePath!~^/iw-admin*;ga:pagePath!~^/[A-z-]+/$'

    def __unicode__(self):
        return self.title

    #  save data passed by the mnagement command to the model
    @classmethod
    def process_data(self, data, date):
        # types = self.retrieve_types()
        for page_path, page_title, page_views in data['rows']:

            obj = self.get_object(page_path)
            # print page_path
            if obj is not None:
                data, created = self.objects.get_or_create(
                    item_url=page_path,
                    defaults={'no_of_views': page_views})
                data.pulled_date = date
                data.content_type = ContentType.objects.get_for_model(obj)
                data.object_id = obj.id
                data.content_object = obj
                data.title = obj.title
                data.save()

    @classmethod
    def get_object(self, url):
        try:
            obj_info = ObjectUrl.objects.get(url=url)
            content_type = obj_info.content_type
            model = apps.get_model(content_type.app_label, content_type.model)
            return model.objects.get(pk=obj_info.object_id)
        except:
            return None


# A Model to define Google Analytic
class Account(models.Model):
    account_name = models.CharField(max_length=255)
    # Service_account and Private key should be stored encrypted
    # Encryption code is defined on the admin save method.
    service_account = models.TextField()
    private_key = models.TextField()

    def __unicode__(self):
        return self.account_name
