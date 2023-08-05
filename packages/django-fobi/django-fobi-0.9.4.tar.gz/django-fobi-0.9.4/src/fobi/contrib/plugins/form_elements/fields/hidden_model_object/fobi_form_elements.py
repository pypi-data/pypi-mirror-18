from django.forms.models import ModelChoiceField
from django.forms.widgets import HiddenInput
from django.utils.translation import ugettext_lazy as _

from fobi.base import (
    FormFieldPlugin, form_element_plugin_registry, get_theme
)
from fobi.helpers import safe_text, get_model_name_for_object

from nine.versions import DJANGO_GTE_1_7

from . import UID
from .forms import HiddenModelObjectInputForm

if DJANGO_GTE_1_7:
    from django.apps import apps
    get_model = apps.get_model
else:
    from django.db.models import get_model

__title__ = 'fobi.contrib.plugins.form_elements.fields.' \
            'hidden_model_object.fobi_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('HiddenModelObjectInputPlugin',)

theme = get_theme(request=None, as_instance=True)


class HiddenModelObjectInputPlugin(FormFieldPlugin):
    """Hidden model object field plugin."""

    uid = UID
    name = _("Hidden model object")
    group = _("Fields")
    form = HiddenModelObjectInputForm
    is_hidden = True

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        app_label, model_name = self.data.model.split('.')
        model = get_model(app_label, model_name)
        queryset = model._default_manager.all()

        field_kwargs = {
            'label': self.data.label,
            'help_text': self.data.help_text,
            'initial': self.data.initial,
            'required': self.data.required,
            'queryset': queryset,
            'widget': HiddenInput(
                attrs={'class': theme.form_element_html_class}
            ),
        }

        return [(self.data.name, ModelChoiceField, field_kwargs)]

    def submit_plugin_form_data(self, form_entry, request, form):
        """Submit plugin form data/process.

        :param fobi.models.FormEntry form_entry: Instance of
            ``fobi.models.FormEntry``.
        :param django.http.HttpRequest request:
        :param django.forms.Form form:
        """
        # Get the object
        obj = form.cleaned_data.get(self.data.name, None)
        if obj:
            value = '{0}.{1}.{2}.{3}'.format(
                obj._meta.app_label,
                get_model_name_for_object(obj),
                obj.pk,
                safe_text(obj)
            )

            # Overwrite ``cleaned_data`` of the ``form`` with object
            # qualifier.
            form.cleaned_data[self.data.name] = value

        # It's critically important to return the ``form`` with updated
        # ``cleaned_data``
        return form


form_element_plugin_registry.register(HiddenModelObjectInputPlugin)
