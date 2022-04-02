import json

from flambda_app import helper


class AbstractVO:
    def __str__(self):
        return self.to_json()

    def __repr__(self):
        return self.to_json()

    def to_dict(self, force_str=False):
        return helper.to_dict(self, force_str)

    def to_json(self):
        return json.dumps(self.to_dict(force_str=False))

    def __getitem__(self, n):
        """
        Permite o objeto ser iterado
        :param n:
        :return:
        """
        count = len(self.__dict__)
        items = list(self.__dict__)
        if n >= count:
            raise IndexError("Object has no item %s" % (n,))
        else:
            return items[n]

    def get(self, k, d=None):
        """ Object.get(k[,d]) -> Object[k] if k in Object, else d.  d defaults to None. """
        return self.__dict__[k] if k in self.__dict__.keys() else d

    def keys(self):
        """ Object.keys() -> a set-like object providing a view on Object's keys """
        return self.__dict__.keys()

    def values(self):
        """ Object.values() -> an object providing a view on Object's values """
        return self.__dict__.values()
