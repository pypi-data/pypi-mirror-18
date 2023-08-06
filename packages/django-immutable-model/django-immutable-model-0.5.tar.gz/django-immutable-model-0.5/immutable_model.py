from django.db import models
from collections import namedtuple
import collections


def _to_hashable(_obj):
    try:
        hash(_obj)
        return _obj
    except:
        pass

    if isinstance(_obj, dict):
        assert all(isinstance(k, collections.Hashable)
                   for k in _obj), "Key should be Hashable"
        values = {k: _to_hashable(_obj[k]) for k in _obj}
        return namedtuple('GenericDict', values.keys(), rename=True)(*values.values())

    if isinstance(_obj, (tuple, list)):
        return tuple(_to_hashable(k) for k in _obj)

    raise NotImplementedError()


class ImmutableModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True, editable=False)

    def to_nametuple(self):
        v = {k: self.__dict__[k] for k in self.__dict__ if k[0] != "_"}
        return _to_hashable(v)

    def __hash__(self):
        return str(hash(self.to_nametuple()))

    def __unicode__(self):
        return u"{}<{}>".format(self.__class__.__name__, self.id)

    def replace(self, **kwargs):
        v = {k: self.__dict__[k]
             for k in self.__dict__ if k[0] != "_" and k != "id"}
        v.update(kwargs)
        return self.__class__.objects.create(**v)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.pk = self.__hash__()
            try:
                # don't need to save if the model is exist already
                self.__class__.objects.get(id=self.pk)
            except:
                super(ImmutableModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
