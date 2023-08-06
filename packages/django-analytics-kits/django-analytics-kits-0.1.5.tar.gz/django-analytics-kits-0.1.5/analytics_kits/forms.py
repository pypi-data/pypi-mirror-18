from django.forms import ModelForm
from django.contrib.admin import widgets

import models
from utils import KitCrypt


class AccountForm(ModelForm):

    class Meta:
        model = models.Account
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kitcrypt = KitCrypt()

        if 'instance' in kwargs and kwargs['instance']:
            initial = {}
            if 'initial' in kwargs:
                initial = kwargs['initial']
            instance = kwargs['instance']
            initial['private_key'] = kitcrypt.decrypt(instance.private_key)
            initial['service_account'] = kitcrypt.decrypt(
                instance.service_account)
            kwargs['initial'] = initial

        super(AccountForm, self).__init__(*args, **kwargs)
        self.fields['service_account'].widget = widgets.AdminTextInputWidget()
