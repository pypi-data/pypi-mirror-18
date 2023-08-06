import os
from itertools import chain

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.deconstruct import deconstructible

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


class FileSystemStorageFactory():

    @classmethod
    def build(cls, directory):
        fs = FileSystemStorage(location=directory)
        return fs

'''
@deconstructible
class LocalStorage(FileSystemStorage):

    """
    A FileSystemStorage which normalizes extensions for images.
    Comes from http://www.djangosnippets.org/snippets/965/
    """

    def __init__(self, dir):

    def save(self, name, content, max_length=None):
        dirname = os.path.dirname(name)
        basename = os.path.basename(name)

        # Does the basename already have an extension? If so, replace it.
        # bare as in without extension
        basename, _ = os.path.splitext(basename)
        # basename = bare_basename + '.' + extension

        name = os.path.join(dirname, basename)
        return super(ImageStorage, self).save(name, content)
'''


class AbstractPersistanceManager(models.Manager):

    def all_persisted_files(self, directory=None,
                            relative_to_root=False, UPLOAD_DIR='testing/'):
        if directory is None:
            directory = os.path.join(settings.MEDIA_ROOT, UPLOAD_DIR)
        all_files = []
        for root, dirs, files in os.walk(directory):
            for filename in files:
                rel_path = os.path.join(root, filename)
                if relative_to_root:
                    rel_path = os.path.relpath(
                        rel_path, start=settings.MEDIA_ROOT)
                all_files.append(rel_path)
        return all_files

    def group_persisted_files_by_hash(self):
        file_hash_groups = {}
        for f in self.all_persisted_files():
            file_hash = f.split('/')[-1].split('_')[0]
            if not file_hash_groups.get(file_hash):
                file_hash_groups[file_hash] = [f]
            else:
                file_hash_groups[file_hash].append(f)
        return file_hash_groups

    def all_duplicated_files(self):
        return list(chain.from_iterable(
            [i[1:] for i in self.group_persisted_files_by_hash().values()]))

    def all_unique_files(self):
        return [i[0] for i in self.group_persisted_files_by_hash().values()]

    def unreferenced_files(self, directory=None):
        all_files = set(self.all_persisted_files(directory=directory))
        files_referenced = set(self.filter(
            object_file__in=all_files).values_list('object_file', flat=True))
        files_unreferenced = all_files - files_referenced
        return files_unreferenced

    def empty_records(self):
        all_files = self.all_persisted_files()
        empty_records = self.exclude(object_file__in=all_files).all()
        return empty_records


class EstimatorManager(AbstractPersistanceManager):

    def all_persisted_files(self, *args, **kwargs):
        from estimators.models.estimators import ESTIMATOR_DIR
        return super().all_persisted_files(*args, UPLOAD_DIR=ESTIMATOR_DIR, **kwargs)


class DataSetManager(AbstractPersistanceManager):

    def all_persisted_files(self, *args, **kwargs):
        from estimators.models.datasets import DATASET_DIR
        return super().all_persisted_files(*args, UPLOAD_DIR=DATASET_DIR, **kwargs)


class temp():

    @classmethod
    def delete_empty_records(cls):
        empty_records = cls.objects.empty_records()
        return empty_records.delete()

    @classmethod
    def delete_unreferenced_files(cls):
        unreferenced_files = cls.objects.unreferenced_files()
        for unreferenced_path in unreferenced_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, unreferenced_path))
        return len(unreferenced_files)

    @classmethod
    def delete_duplicated_files(cls):
        duplicated_files = cls.objects.all_duplicated_files()
        for duplicated_path in duplicated_files:
            os.remove(os.path.join(settings.MEDIA_ROOT, duplicated_path))
        return len(duplicated_files)

    @classmethod
    def load_unreferenced_files(cls, directory=None):
        unreferenced_files = cls.objects.unreferenced_files(
            directory=directory)
        for filename in unreferenced_files:
            obj = cls.create_from_file(filename)
            obj.save()
        return len(unreferenced_files)
