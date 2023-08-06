from __future__ import unicode_literals

from itertools import chain

from django.forms.widgets import Select
from django.utils.encoding import force_text
from django.utils.html import conditional_escape, escape, format_html
from django.utils.safestring import mark_safe


class SelectBy(Select):
    select_by = None
    parent = None

    def __init__(self, attrs=None, choices=(), select_by=None):
        super(Select, self).__init__(attrs)
        self.choices = list(choices)
        self.select_by = select_by

    def render_option(self, selected_choices, option_value, option_label):
        parent = self.parent if self.parent else ''
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            if not self.allow_multiple_selected:
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html(u'<option data-parent-id="{3}" value="{0}"{1}>{2}</option>'.format(escape(option_value),
                                                                                              selected_html,
                                                                                              conditional_escape(
                                                                                                  option_label),
                                                                                              parent))

    def render_options(self, choices, selected_choices):
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                if self.select_by and option_value:
                    self.parent = getattr(self.choices, 'queryset').filter(pk=option_value).values_list(self.select_by,
                                                                                                        flat=True)[0]
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)