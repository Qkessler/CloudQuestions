import os
import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError


def validate_markdown(upload):
    # Make uploaded file accessible for analysis by saving in tmp
    tmp_path = f'tmp/{upload.name[2:]}'
    default_storage.save(tmp_path, ContentFile(upload.file.read()))
    full_tmp_path = os.path.join(settings.MEDIA_ROOT, tmp_path)
    file_type = magic.from_file(full_tmp_path, mime=True)
    default_storage.delete(tmp_path)
    if file_type not in 'text/plain':
        raise ValidationError('File type not supported: md (Markdown) only.')
