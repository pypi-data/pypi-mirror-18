from django.contrib import admin

import models
import forms
from utils import KitCrypt


class AcountsAdmin(admin.ModelAdmin):

    form = forms.AccountForm

    def save_model(self, request, obj, form, change):
        super(AcountsAdmin, self).save_model(request, obj, form, change)
        kitcrypt = KitCrypt()
        if 'private_key' in form.data and form.data['private_key']:
            obj.private_key = kitcrypt.encrypt(str(form.data['private_key']))
        if 'service_account' in form.data and form.data['service_account']:
            obj.service_account = kitcrypt.encrypt(
                str(form.data['service_account']))

        obj.save()

admin.site.register(models.Account, AcountsAdmin)

admin.site.register(models.ObjectUrl)
