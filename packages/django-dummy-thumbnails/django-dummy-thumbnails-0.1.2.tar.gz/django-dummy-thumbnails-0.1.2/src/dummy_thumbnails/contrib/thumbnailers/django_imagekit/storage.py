import os

from django.core.files.storage import FileSystemStorage
from django.utils._os import safe_join

from ....base import get_random_image

__title__ = 'dummy_thumbnails.contrib.thumbnailers.django_imagekit.storage'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'DummyThumbnailsStorage',
)


class DummyThumbnailsStorage(FileSystemStorage):
    """DummyThumbnails storage."""

    def path(self, name):
        path = safe_join(self.location, name)
        if not (name and (os.path.exists(path)
                          or os.path.isfile(path))):
            path = get_random_image()
        return path
