from django.test import TestCase, SimpleTestCase
from analytics_kits import utils
from analytics_kits import models as ak_models
import models
import mock


class UtilsTests(SimpleTestCase):

    kitcrypt = utils.KitCrypt()

    def test_encrypt(self):
        encrypted = self.kitcrypt.encrypt("SmallMediaLab")
        self.assertNotEqual("SmallMediaLab", encrypted)

    def test_decrypt(self):
        encrypted = self.kitcrypt.encrypt("SmallMediaLab")
        decrypted = self.kitcrypt.decrypt(encrypted)
        self.assertEqual("SmallMediaLab", decrypted)


class ModelTests(TestCase):

    def test_mixin_model_save_method(self):
        count_1 = ak_models.ObjectUrl.objects.all().count()
        content = models.TestContent(**{'title': 'Foo-Bar'})
        content.save()
        count_2 = ak_models.ObjectUrl.objects.all().count()
        self.assertNotEqual(count_1, count_2)

    @mock.patch('analytics_kits.models.logging')
    def test_mixin_model_loggig_error(self, mock_logging):
        content = models.BadContentModel(**{'title': 'Foo-Bar'})
        content.save()
        self.assertTrue(mock_logging.error.called)
