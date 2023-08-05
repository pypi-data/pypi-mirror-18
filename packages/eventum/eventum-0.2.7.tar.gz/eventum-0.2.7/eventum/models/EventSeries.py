"""
.. module:: EventSeries
    :synopsis: A database model for an event series.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""

from datetime import datetime
from mongoengine import (Document, DateTimeField, ReferenceField, IntField,
                         ListField, StringField, BooleanField, ValidationError)
from eventum.models import BaseEventumDocument
from eventum.models.fields import DateField

now = datetime.now


class EventSeries(Document, BaseEventumDocument):
    """A model that stores the recurrence information for a recurring event
    series.

    :ivar date_created: :class:`mongoengine.fields.DateTimeField` - The date
        when the series was created.
    :ivar date_modified: :class:`mongoengine.fields.DateTimeField` - The date
        when the series was last modified
    :ivar slug: :class:`mongoengine.fields.StringField` - The URL slug for this
        event. **Note:** this slug is shared across all
        :class:`~app.models.Event` s in this series.  This is not the event's
        unique URL, rather the slug that is unique between series objects.
    :ivar events: :class:`mongoengine.fields.ListField` - A list of
        :class:`~app.models.Event` s in this series.
    :ivar frequency: :class:`mongoengine.fields.StringField` - The interval of
        the occurrence. Can only take the value ``"weekly"``.
    :ivar every: :class:`mongoengine.fields.IntField` - The number of
        ``frequency`` units after which the event repeats. For example,
        ``frequency = "weekly"`` and ``every = 2`` indicates that the event
        occurs every two weeks.
    :ivar ends_after: :class:`mongoengine.fields.BooleanField` - True if the
        event ends after a specific number of occurences.  Must be set opposite
        to ``ends_on``.
    :ivar ends_on: :class:`mongoengine.fields.BooleanField` - True if the event
        ends on a certain date. Must be set opposite to ``ends_after``.
    :ivar num_occurrences: :class:`mongoengine.fields.IntField` - The number of
        occurrences for a recurring event.  Should be set only if
        ``ends_after`` is ``True``.
    :ivar recurrence_end_date: :class:`DateField` - The date that the
        recurrence ends on.  Should be set only if ``ends_on`` is ``True``.
    :ivar recurrence_summary: :class:`mongoengine.fields.StringField` - A plain
        English explanation of the recurrence. Generated in JavaScript but
        stored here.
    :ivar gcal_id: :class:`mongoengine.fields.StringField` - The ID for this
        event series on Google Calendar.  In Google Calendar API responses,
        this is stored as the ``id`` field for events. If this field is None,
        then we never got a proper response from Google Calendar when (if) we
        made a request to create it there. It most likely does not exist on
        Google Calendar.  This is the same as the ``gcal_id`` of the first
        event in the series.
    """

    # MongoEngine ORM metadata
    meta = {}

    date_created = DateTimeField(required=True, default=now)
    date_modified = DateTimeField(required=True, default=now)
    slug = StringField(required=True, max_length=255)
    events = ListField(ReferenceField("Event"))
    frequency = StringField(default="weekly")
    every = IntField(min_value=1, max_value=30)
    ends_after = BooleanField(default=True)
    ends_on = BooleanField(default=False)
    num_occurrences = IntField(default=1)
    recurrence_end_date = DateField()
    recurrence_summary = StringField()
    gcal_id = StringField()  # ID of the first event in the series

    def delete_one(self, event):
        """Deletes ``event`` after removing it from the series.

        :param event: The event to delete.
        :type event: :class:`~app.models.Event`
        """
        self.events.remove(event)
        event.delete()
        self.save()

    def delete_all_except(self, event):
        """Deletes all events in the series except ``event``, and then deletes
        the series. Should be called when an event's recurrence is disabled.

        :param event: The event to delete.
        :type event: :class:`~app.models.Event`
        """
        for e in self.events[:]:
            if e != event:
                e.delete()
        event.parent_series = None
        self.delete()

    def delete_all(self):
        """Deletes all events in the series, and the series itself."""
        for e in self.events:
            e.delete()
        self.delete()

    def clean(self):
        """Called by Mongoengine on every ``.save()`` to the object.

        Update date_modified, and ensure that exactly one of `ends_after`
        and `ends_on` is True at a time.

        :raises: :class:`wtforms.validators.ValidationError`
        """
        self.date_modified = now()

        if self.ends_after == self.ends_on:
            raise ValidationError("ends_on and ends_after should not share a "
                                  "value.")
