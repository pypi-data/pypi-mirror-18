"""
.. module:: DeleteEventForm
    :synopsis: A form for deleting an event or event series.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""

from flask.ext.wtf import Form
from wtforms import BooleanField


class DeleteEventForm(Form):
    """A form for deleting an event.

    :ivar delete_all: :class:`wtforms.fields.BooleanField` - True if the event
        is recurring and all events in the series should be deleted.
    """
    delete_all = BooleanField('Delete All', default=False)
