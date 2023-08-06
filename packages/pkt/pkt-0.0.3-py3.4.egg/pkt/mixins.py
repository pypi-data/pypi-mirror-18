class ComparableMixin(object):
    def __eq__(self, other):
        return self.to_immutable() == other.to_immutable()

    def to_immutable(self):
        raise NotImplementedError()