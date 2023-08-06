from django.db import models


class DBFile(models.Model):
    """ Model to store and access uploaded files """

    # This is kept as `name` and not something like `md5` because the file
    # operations pass around `name` as the identifier, so it's kept the same
    # to make sense.
    name = models.CharField(max_length=100, primary_key=True)

    # file data
    content_type = models.CharField(max_length=100)
    b64 = models.TextField()

    def __unicode__(self):
        return unicode(self.name)
