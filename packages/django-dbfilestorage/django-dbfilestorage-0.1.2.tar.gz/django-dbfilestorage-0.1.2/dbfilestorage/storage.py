import mimetypes
import logging
import hashlib

from django.db.transaction import atomic
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse

from .models import DBFile

L = logging.getLogger(__name__)


class DBFileStorage(Storage):
    """
        This is the Test Database file upload storage backend.
        This is used so that in our test database we always have uploaded
         files.

        To read more about how to set it up and configure it:
            https://docs.djangoproject.com/en/1.8/howto/custom-file-storage
    """

    def _open(self, name, mode='rb'):
        the_file = DBFile.objects.get(pk=name)
        return ContentFile(the_file.b64.decode('base64'))

    @atomic
    def _save(self, name, content, max_length=None):
        """
           The save method does most of the 'magic'.
           It stores the contents of the file as a base64 string.
           It then takes the filename, and tries to get the mimetype from that
            (for rendering)
           Then it takes the md5 of the read file and uses that as the "unique"
           key to access the file.
           Then it checks if the file exists and if it doesn't, it will create
           the entry in the database.

           :return str: the name(md5) to look up the file by.
        """
        ct = None
        if hasattr(content.file, "read"):
            read_data = content.file.read()
        else:
            read_data = content.file.encode('utf8')
        b64 = read_data.encode('base64')

        # Try to get the real content_type if applicable.
        try:
            if hasattr(content, 'content_type'):
                ct = content.content_type
            elif hasattr(content.file, 'content_type'):
                ct = content.file.content_type
        except AttributeError:
            pass

        # USE mimetypes.guess_type as a fallback.
        if ct is None:
            # https://docs.python.org/2/library/mimetypes.html
            ct = mimetypes.guess_type(name)[0]

        # After we get the mimetype by name potentially, mangle it.
        name = hashlib.md5(read_data).hexdigest()

        # create the file, or just return name if the exact file already exists
        if not DBFile.objects.filter(pk=name).exists():
            the_file = DBFile(
                name=name,
                content_type=ct,
                b64=b64)
            the_file.save()
        return name

    def get_available_name(self, name, max_length=None):
        return name

    def path(self, name):
        return name

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        DBFile.objects.get(pk=name).delete()

    def exists(self, name):
        return DBFile.objects.filter(pk=name).exists()

    def size(self, name):
        dbf = DBFile.objects.get(pk=name)
        return len(dbf.b64)

    def url(self, name):
        return reverse('dbstorage_file', args=(name,))
