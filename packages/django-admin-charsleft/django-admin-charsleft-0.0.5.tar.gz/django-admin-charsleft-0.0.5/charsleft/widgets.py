# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.template.loader import get_template
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage

from django.forms.utils import flatatt


class MediaMixin(object):

    class Media:
        css = {
            'screen': (staticfiles_storage.url('charsleft/css/charsleft.css',),)
        }
        js = (staticfiles_storage.url('charsleft/js/charsleft.js'),)

class CharsLeftCharFieldWidget(forms.TextInput, MediaMixin):

    tpl = get_template('charsleft/widgets/charfield.html')

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        if value != '':
            final_attrs['value'] = force_unicode(self._format_value(value))

        maxlength = final_attrs.get('maxlength')

        if not maxlength:
            return mark_safe(u'<input%s />' % flatatt(final_attrs))

        current = force_unicode(int(maxlength) - len(value))

        return mark_safe(self.tpl.render({
            'attrs': flatatt(final_attrs),
            'current': current,
            'maxlength': int(maxlength),
        }))


class CharsLeftTextFieldWidget(forms.TextInput, MediaMixin):

    tpl = get_template('charsleft/widgets/textfield.html')

    def render(self, name, value, attrs=None):

        if value is None:
            value = ''

        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        maxlength = final_attrs.get('maxlength')

        if not maxlength:
            return mark_safe('<textarea %s >%s</textarea>' % (flatatt(final_attrs), value))

        final_attrs['cols'] = 80
        final_attrs['rows'] = int(int(maxlength)/100) + 1
        current = force_unicode(int(maxlength) - len(value))

        return mark_safe(self.tpl.render({
            'attrs': flatatt(final_attrs),
            'current': current,
            'value': value,
            'maxlength': int(maxlength),
        }))
