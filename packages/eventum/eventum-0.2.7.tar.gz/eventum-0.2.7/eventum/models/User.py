"""
.. module:: User
    :synopsis: A user database model.

.. moduleauthor:: Dan Schlosser <dan@schlosser.io>
"""

import re
from datetime import datetime
from flask import url_for, current_app
from mongoengine import (Document, StringField, ReferenceField, EmailField,
                         ListField, URLField, DictField, DateTimeField)
from eventum.lib.regex import Regex
from eventum.models import BaseEventumDocument

now = datetime.now

# Maps valid values for the ``user_type`` field on the User object to
# dictionaries of privileges that are assocaited with that user type.
USER_TYPES = {
    "fake_user": {
        "edit": False,
        "publish": False,
        "admin": False
    },
    "editor": {
        "edit": True,
        "publish": False,
        "admin": False
    },
    "publisher": {
        "edit": True,
        "publish": True,
        "admin": False
    },
    "admin": {
        "edit": True,
        "publish": True,
        "admin": True
    }
}
USER_TYPE_REGEX = "({})".format('|'.join(USER_TYPES.keys()))


class User(Document, BaseEventumDocument):
    """A user model.

    The :class:`User` object is only created once the user logs in for the
    first time and confirms the details of their account.
    :ivar date_created: :class:`mongoengine.fields.DateTimeField` - The date
        that this user was created.
    :ivar date_modified: :class:`mongoengine.fields.DateTimeField` - The date
        the this user was last modified.
    :ivar gplus_id: :class:`mongoengine.fields.StringField` - The Google+ ID
        for this user.  It's what we use in the Google+ authentication.
    :ivar name: :class:`mongoengine.fields.StringField` - The user's name.
    :ivar slug: :class:`mongoengine.fields.StringField` - A URL slug  their
        internal profile page.
    :ivar email: :class:`mongoengine.fields.EmailField` - The user's email
        address.
    :ivar roles: :class:`mongoengine.fields.ListField` of
        :class:`mongoengine.fields.StringField` - A list of roles that the user
        has.
    :ivar privileges: :class:`mongoengine.fields.DictField` - A dictionary of
        privileges that the user has.  Often determined soley by their
        ``user_type``.
    :ivar image_url: :class:`mongoengine.fields.URLField` - The URL of the
        profile picture for the user's profile picture.
    :ivar image: :class:`mongoengine.fields.ReferenceField` - The local image
        for the user's profile picture.
    :ivar user_type: :class:`mongoengine.fields.StringField` - The type of the
        user. Can either be ``"fake_user"``, ``"editor"``, ``"publisher"``, or
        ``"admin"``.  The selection of user type determines their
        ``privileges``.
    :ivar last_logon: :class:`mongoengine.fields.DateTimeField` - The date of
        this user's last logon.
    """

    date_created = DateTimeField(required=True, default=now)
    date_modified = DateTimeField(required=True, default=now)
    gplus_id = StringField(required=True, unique=True)
    name = StringField(required=True, max_length=510)
    slug = StringField(required=True,
                       max_length=510,
                       unique=True,
                       regex=Regex.SLUG_REGEX)
    email = EmailField(required=True, unique=True)
    roles = ListField(StringField(db_field="role"), default=list)
    privileges = DictField(required=True, default={})
    image_url = URLField()
    image = ReferenceField('Image')
    user_type = StringField(default='editor',
                            regex=USER_TYPE_REGEX)
    last_logon = DateTimeField()

    # MongoEngine ORM metadata
    meta = {
        'allow_inheritance': True,
        'indexes': ['email', 'gplus_id']
    }

    def can(self, privilege):
        """Returns True if the user has ``privilege``.

        :returns: True if the user has ``privilege``
        :rtype: bool
        """
        return self.privileges.get(privilege)

    def get_profile_picture(self, size=50):
        """Returns the url to the profile picture for the user.

        TODO: This method needs major fixing.  What's going on with that URL?

        :param int size: The size of the image to pass, if the size can be
            changed.

        :returns: The URL of the image.
        :rtype: str
        """
        if self.image:
            return self.image.url()
        if not self.image_url:
            # Import app in the function body to avoid importing `None` when
            # the module is first loaded.
            return url_for(
                'eventum.static',
                filename=current_app.config['EVENTUM_DEFAULT_PROFILE_PICTURE'])
        if "googleusercontent.com" in self.image_url:
            return self.image_url + str(size)
        return self.image_url

    def register_login(self):
        """Update the model as having logged in."""
        self.last_logon = now()

    def clean(self):
        """Called by Mongoengine on every ``.save()`` to the object.

        Update date_modified and apply privileges shorthand notation.

        :raises: :class:`wtforms.validators.ValidationError`
        """
        self.date_modified = now()

        # Update self.privileges with one of the USER_TYPES dictionaries
        self.privileges.update(USER_TYPES[self.user_type])

        # Update the slug for the user (used in URLs)
        new_slug = self.name.lower().replace(' ', '-')
        new_slug = re.sub(r"\'|\.|\_|", "", new_slug)
        if User.objects(slug=new_slug).count() > 0:
            i = 2
            new_slug = new_slug + "-{}".format(i)
            while User.objects(slug=new_slug).count() > 0:
                i += 1
                new_slug = re.sub(r"-([0-9])*$", "-{}".format(i), new_slug)
        self.slug = new_slug

        if self.image_url and "googleusercontent.com" in self.image_url:
            self.image_url = re.sub(r"sz=([0-9]*)$", "sz=", self.image_url)

    def id_str(self):
        """The id of this object, as a string.

        :returns: The id
        :rtype: str
        """
        return str(self.id)

    def role(self):
        """Returns the role of the user, in plain English.  It is either
        ``"Admin"``, ``"Publisher"``, ``"Editor"``, or ``"Fake User"``.

        :returns: The role.
        :rtype: str
        """
        if self.can('admin'):
            return "Admin"
        if self.can('publish'):
            return "Publisher"
        if self.can('edit'):
            return "Editor"
        return "Fake User"

    def __repr__(self):
        """The representation of this user.

        :returns: The user's details.
        :rtype: str
        """
        return ('User(id=%r, name=%r, email=%r, roles=%r, privileges=%r, '
                'gplus_id=%r, date_created=%r)' %
                (self.id, self.name, self.email, self.roles,
                 self.privileges, self.gplus_id, self.date_created))

    def __unicode__(self):
        """This user, as a unicode string.

        :returns: The user encoded as a string.
        :rtype: str
        """
        if self.can('admin'):
            return '%r <%r> (Admin)' % (self.name, self.email)
        if self.can('publish'):
            return '%r <%r> (Publisher)' % (self.name, self.email)
        if self.can('edit'):
            return '%r <%r> (Editor)' % (self.name, self.email)
        else:
            return '%r <%r> (Fake User)' % (self.name, self.email)
