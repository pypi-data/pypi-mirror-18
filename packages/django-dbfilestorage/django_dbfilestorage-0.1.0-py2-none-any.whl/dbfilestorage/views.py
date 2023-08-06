from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import DBFile


def show_file(request, name):
    """
        Get the file object referenced by :name:
        Render the decoded base64 representation of the file,
            applying the content_type (or closest representation)

        :return HttpResponse: Rendered file
    """
    dbf = get_object_or_404(DBFile, pk=name)
    return HttpResponse(
        dbf.b64.decode('base64'),
        content_type=dbf.content_type)
