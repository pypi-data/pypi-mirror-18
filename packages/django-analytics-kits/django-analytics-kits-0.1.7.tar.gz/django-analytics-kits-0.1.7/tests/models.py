from django.db import models
from analytics_kits import models as ak_models


# A content model inherited from AnalyiticsKitsMixin should have
# a get_absolute_url method
class BadContentModel(ak_models.AnalyiticsKitsMixin):
    title = models.CharField(max_length=255)


class TestContent(ak_models.AnalyiticsKitsMixin):
    title = models.CharField(max_length=255)

    def get_absolute_url(self):
        return '/test_content/%d' % self.id
