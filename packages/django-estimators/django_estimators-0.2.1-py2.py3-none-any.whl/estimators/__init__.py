from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

ESTIMATOR_DIR = getattr(settings, "ESTIMATOR_DIR", 'estimators/')
DATASET_DIR = getattr(settings, "DATASET_DIR", 'datasets/')

files_map = {
    '_estimator': ESTIMATOR_DIR,
    '_data': DATASET_DIR,
}


def get_upload_path(instance, filename):
    directory = files_map[instance._object_property_name]
    full_path = os.path.join(directory, filename)
    return full_path


def get_storage():
    ''' return configured Storage '''
    return FileSystemStorage(location=settings.MEDIA_ROOT)
