import httplib2

from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import crypt
from datetime import datetime, timedelta

from analytics_kits import models
from analytics_kits.utils import KitCrypt


class Command(BaseCommand):

    # python manage.py most_popular -a en_site -m MostPopular

    def add_arguments(self, parser):
        # App arguments
        parser.add_argument(
            '--app', '-a', dest='data_app',
            help='The app which contains your data model')

        # Model arguments
        parser.add_argument(
            '--model', '-m', dest='data_model',
            help='The data model defining your query')

        # Model arguments
        parser.add_argument(
            '--view', dest='view_id',
            help='Google Analytic view id')

        # Account name arguments
        parser.add_argument(
            '--account', dest='account_name',
            help='Google Analytic account name')

    help = 'Imports the most visited pages data from analytics'

    def handle(self, **options):
        data_model = options['data_model']
        data_app = options['data_app']
        view_id = options['view_id']
        account_name = options['account_name']

        # Ensure we have an app and a model
        if not data_model or not data_app or not view_id:
            raise CommandError(
                "Please specify application, model and the view id.")

        elif apps.get_model(data_app, data_model) is None:
            raise CommandError(
                "Unable to import model (%s) from (%s)" % (
                    data_model, data_app))

        else:
            data_model = apps.get_model(data_app, data_model)

        now = datetime.now()
        end_date = datetime(now.year, now.month, now.day, now.hour, now.minute)
        # 24 hours prior to now
        start_date = end_date-timedelta(days=1)

        self._load_data(
            data_model, start_date, end_date, view_id, account_name)

    @staticmethod
    def _load_data(data_model, start_date, end_date, view_id, account_name):

        kitcrypt = KitCrypt()

        account = models.Account.objects.get(
            account_name=account_name)
        key = kitcrypt.decrypt(account.private_key)
        signer = crypt.Signer.from_string(key)

        credentials = ServiceAccountCredentials(
            kitcrypt.decrypt(account.service_account), signer,
            scopes='https://www.googleapis.com/auth/analytics.readonly')

        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('analytics', 'v3', http=http)

        data_query = service.data().ga().get(
            ids='ga:%s' % view_id,
            metrics=data_model.get_metrics(),
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            dimensions=data_model.get_dimensions(),
            sort=data_model.get_sort(),
            filters=data_model.get_filters(),
            max_results=data_model.get_results_count())

        feed = data_query.execute()

        if 'rows' in feed:

            data_model.process_data(feed, start_date)
            print "%s - %s - Processed data" % (
                start_date, data_model.__name__)
        else:
            print "%s - %s - No data available" % (
                start_date, data_model.__name__)
