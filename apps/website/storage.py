# coding=utf-8
# Author: Christian Douglas <christian.douglas.alcantara@gmail.com>
import unicodedata

from django.core.files.storage import FileSystemStorage
import subprocess
from mimetypes import MimeTypes
import tempfile
from django.conf import settings
import os


def compress_pdf(name):
    full_filename = os.path.join(settings.MEDIA_ROOT, name)
    tmp_file = tempfile.mktemp()

    if not os.path.exists(os.path.dirname(full_filename)):
        os.makedirs(os.path.dirname(full_filename))

    if os.path.exists(full_filename):
        mtype = MimeTypes().guess_type(full_filename)
        if mtype[0] == 'application/pdf':
            subprocess.call(['ps2pdf', full_filename, tmp_file])
            subprocess.call(['mv', '-f', tmp_file, full_filename])
            subprocess.call(['rm', '-rf', tmp_file])
    return name


class ASCIIFileSystemStorage(FileSystemStorage):
    """
    Convert unicode characters in name to ASCII characters.
    """
    def get_valid_name(self, name):
        name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore')
        return super(ASCIIFileSystemStorage, self).get_valid_name(name)

    def _save(self, name, content):
        ret = super(ASCIIFileSystemStorage, self)._save(name, content)
        compress_pdf(name)
        return ret
