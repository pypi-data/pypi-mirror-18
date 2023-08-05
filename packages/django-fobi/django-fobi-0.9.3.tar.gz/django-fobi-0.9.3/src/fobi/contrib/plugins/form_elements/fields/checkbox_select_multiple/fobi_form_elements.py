from django.forms.fields import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _

from fobi.base import FormFieldPlugin, form_element_plugin_registry, get_theme
from fobi.constants import (
    SUBMIT_VALUE_AS_VAL, SUBMIT_VALUE_AS_REPR
)
from fobi.helpers import get_select_field_choices, safe_text

from . import UID
from .forms import CheckboxSelectMultipleInputForm
from .settings import SUBMIT_VALUE_AS

theme = get_theme(request=None, as_instance=True)

__title__ = 'fobi.contrib.plugins.form_elements.fields.' \
            'checkbox_select_multiple.fobi_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('CheckboxSelectMultipleInputPlugin',)


class CheckboxSelectMultipleInputPlugin(FormFieldPlugin):
    """Checkbox select multiple field plugin."""

    uid = UID
    name = _("Checkbox select multiple")
    group = _("Fields")
    form = CheckboxSelectMultipleInputForm

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        choices = get_select_field_choices(self.data.choices)

        field_kwargs = {
            'label': self.data.label,
            'help_text': self.data.help_text,
            'initial': self.data.initial,
            'required': self.data.required,
            'choices': choices,
            'widget': CheckboxSelectMultiple(
                attrs={'class': theme.form_element_html_class}
            ),
        }

        return [(self.data.name, MultipleChoiceField, field_kwargs)]

    def submit_plugin_form_data(self, form_entry, request, form):
        """Submit plugin form data/process.

        :param fobi.models.FormEntry form_entry: Instance of
            ``fobi.models.FormEntry``.
        :param django.http.HttpRequest request:
        :param django.forms.Form form:
        """
        # In case if we should submit value as is, we don't return anything.
        # In other cases, we proceed further.
        if SUBMIT_VALUE_AS != SUBMIT_VALUE_AS_VAL:
            # Get the object
            values = form.cleaned_data.get(self.data.name, None)

            # Get choices
            choices = dict(get_select_field_choices(self.data.choices))

            # Returned value
            ret_values = []

            for value in values:
                # Handle the submitted form value

                if value in choices:
                    label = safe_text(choices.get(value))

                    # Should be returned as repr
                    if SUBMIT_VALUE_AS == SUBMIT_VALUE_AS_REPR:
                        value = label
                    # Should be returned as mix
                    else:
                        value = "{0} ({1})".format(label, value)

                    ret_values.append(value)

            # Overwrite ``cleaned_data`` of the ``form`` with object
            # qualifier.
            form.cleaned_data[self.data.name] = ret_values

            # It's critically important to return the ``form`` with updated
            # ``cleaned_data``
            return form


form_element_plugin_registry.register(CheckboxSelectMultipleInputPlugin)
