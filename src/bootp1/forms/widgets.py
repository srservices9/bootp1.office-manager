"""Widget rendering the <input> together with its <datalist>."""

from markupsafe import Markup, escape
from wtforms.widgets import TextInput

__all__ = ["DatalistInput"]


class DatalistInput(TextInput):
    """TextInput that also renders an attached HTML5 ``<datalist>``.

    The input gets a ``list`` attribute pointing at a datalist whose id is
    ``<field.id>_list``. Override per-render with ``list_id=...`` if two
    fields must share one datalist::

        {{ form.phone(class="form-control", list_id="shared_numbers") }}

    All other keyword arguments are rendered as input attributes, exactly
    like the stock ``TextInput``.
    """

    def __call__(self, field, **kwargs):
        list_id = kwargs.pop("list_id", None) or "%s_list" % field.id
        kwargs["list"] = list_id

        html = [super(DatalistInput, self).__call__(field, **kwargs)]
        html.append('<datalist id="%s">' % escape(list_id))
        for value, label in field.iter_datalist():
            if label:
                html.append(
                    '<option value="%s">%s</option>' % (escape(value), escape(label))
                )
            else:
                html.append('<option value="%s"></option>' % escape(value))
        html.append("</datalist>")
        return Markup("".join(html))
