import operator

from sqlalchemy.ext.associationproxy import _AssociationSet


class AppenderAssociationSet(_AssociationSet):
    """Subclass `_AssociationSet` to adapt some set methods to that of `AppenderQuery`."""
    def add(self, object_):
        if object_ not in self:
            self.col.append(self._create(object_))

    def extend(self, objects):
        for obj in objects:
            if obj not in self:
                self.col.append(self._create(obj))

    def remove(self, value):
        for member in self.col:
            if self._get(member) == value:
                self.col.remove(member)
                return
        raise KeyError(value)

    def clear(self):
        del self.col[:]


def set_factory(lazy_collection, creator, value_attr, assoc_prox):
    """Factory for set-like `association_proxy` collections.

    Example declaration::
        facets = association_proxy('facets', 'facet', proxy_factory=set_factory)
    """

    # MyObject.<value_attr>
    getter = operator.attrgetter(value_attr)

    # MyObject.<value_attr> = <v>
    def setter(o, v):
        setattr(o, value_attr, v)

    return AppenderAssociationSet(lazy_collection, creator, getter, setter, assoc_prox)
