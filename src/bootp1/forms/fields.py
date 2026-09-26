"""DatalistField — StringField with native <datalist> suggestions."""

from typing import Any, Callable, Iterable, Iterator, Mapping, Tuple, Union

from wtforms import StringField
from wtforms.validators import ValidationError

from .widgets import DatalistInput

__all__ = ["DatalistField"]

DatalistItems = Union[
    Iterable[Any],            # values, or (value, label) pairs
    Mapping[Any, Any],        # value -> label
]
Datalist = Union[DatalistItems, Callable[[], DatalistItems]]


class DatalistField(StringField):
    """StringField whose widget renders a datalist of suggestions.

    ``datalist`` accepts any of:

    * an iterable of strings — ``["111", "222"]``
    * an iterable of ``(value, label)`` pairs — most browsers show the label
      next to the value in the dropdown
    * a dict — ``{"111": "SIM · Sales"}`` (value → label)
    * a zero-argument callable returning any of the above — evaluated at
      render/validation time, so per-request data (e.g. a DB query) can be
      bound in the form definition itself

    Like ``SelectField.choices``, the list can also be assigned after
    construction: ``form.phone.datalist = [...]``.

    A browser datalist only suggests — the user may still type anything. So,
    like ``SelectField``, the field checks on validation that the submitted
    value is one of the datalist values (for pairs — the *value*, not the
    label) and raises "Not a valid choice." otherwise. Pass
    ``validate_choice=False`` to allow free text (suggestions only). An empty
    value is not checked against the list — combine with ``DataRequired`` /
    ``Optional`` as usual.

    ``data`` is always the raw submitted string, as with any text input.
    """

    widget = DatalistInput()

    def __init__(self, label=None, validators=None, datalist=None,
                 validate_choice=True, **kwargs):
        # type: (Any, Any, Datalist, bool, **Any) -> None
        super(DatalistField, self).__init__(label, validators, **kwargs)
        self.datalist = datalist if datalist is not None else []  # type: Datalist
        self.validate_choice = validate_choice

    def iter_datalist(self):
        # type: () -> Iterator[Tuple[Any, Any]]
        """Yield normalized ``(value, label)`` pairs, label may be ''."""
        items = self.datalist() if callable(self.datalist) else self.datalist
        if items is None:
            return
        if isinstance(items, dict):
            items = items.items()
        for item in items:
            if isinstance(item, (tuple, list)):
                yield item[0], item[1] if len(item) > 1 else ""
            else:
                yield item, ""

    def iter_values(self):
        # type: () -> Iterator[Any]
        """Yield the submittable values only."""
        for value, _label in self.iter_datalist():
            yield value

    def pre_validate(self, form):
        if not self.validate_choice or not self.data:
            return
        for value in self.iter_values():
            if str(self.data) == str(value):
                return
        raise ValidationError(self.gettext("Not a valid choice."))
