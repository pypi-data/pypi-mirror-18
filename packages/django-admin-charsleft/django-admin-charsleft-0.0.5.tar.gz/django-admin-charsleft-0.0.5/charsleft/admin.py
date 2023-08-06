# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from .widgets import CharsLeftCharFieldWidget, CharsLeftTextFieldWidget

class CharsLeftAdminMixin(object):

    _formfield_overrides = {
        models.TextField: {
            'widget': CharsLeftTextFieldWidget()
        },
        models.CharField: {
            'widget': CharsLeftCharFieldWidget()
        },
    }

    def __init__(self, *args, **kwargs):
        super(CharsLeftAdminMixin, self).__init__(*args, **kwargs)
        self.formfield_overrides.update(self._formfield_overrides)
