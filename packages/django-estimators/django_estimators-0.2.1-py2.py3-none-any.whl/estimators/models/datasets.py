from django.db import models

from estimators import DATASET_DIR
from estimators.models.base import HashableFileMixin, HashableFileQuerySet


class DataSetQuerySet(HashableFileQuerySet):

    object_property_name = 'data'


class DataSet(HashableFileMixin):

    description = models.CharField(max_length=256)
    _data = None
    _object_property_name = '_data'

    objects = DataSetQuerySet.as_manager()

    DIRECTORY = DATASET_DIR

    class Meta:
        db_table = 'data_sets'

    @property
    def data(self):
        """return the dataframe, and load it into memory if it hasn't been loaded yet"""
        return self.get_object()

    @data.setter
    def data(self, obj):
        self.set_object(obj)

    def save(self, *args, **kwargs):
        self.full_clean(exclude=['description'])
        super().save(*args, **kwargs)

    def __repr__(self):
        return '<Dataset <Id %s - %s>>' % (self.id, str(self.data))
