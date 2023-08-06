import inspect
import types
from abc import ABCMeta, abstractmethod

from rancher.utils import uncamelize

import requests


class Field:

    def __init__(self, default="", cast=str):
        self.values = dict()
        self.default = default
        self.cast = cast

    def __get__(self, instance, owner):
        return self.values.get(instance, self.default)

    def __set__(self, instance, value):
        self.values[instance] = value

    def __delete__(self, instance):
        del self.values[instance]


class JsonMarshable:

    uncamelize = True

    @classmethod
    def get_members(cls):
        members = inspect.getmembers(cls)
        members = filter(lambda e: not e[0].startswith("__"), members)
        members = filter(lambda e: not isinstance(e[1], types.MethodType), members)
        members = filter(lambda e: not (callable(e[1]) and not inspect.isclass(e[1])), members)
        return {name: value for name, value in members}

    @classmethod
    def from_dict(cls, dict_repr):
        members = cls.get_members()
        instance = cls()
        for key, value in instance.repr_items(dict_repr):
            if key in members.keys():
                if members[key] and issubclass(members[key], Model):
                    setattr(instance, key, getattr(cls, key).from_dict(value))
                    continue
                setattr(instance, key, value)
        return instance

    def repr_items(self, representation):
        if isinstance(representation, types.GeneratorType):
            items = representation
        else:
            items = representation.items()
        if self.uncamelize:
            for key, value in items:
                if isinstance(value, dict):
                    value = self.repr_items(value)
                yield uncamelize(key), value
        else:
            yield from items

    def to_dict(self):
        obj = dict()
        for field, value in self.get_members().items():
            if field in JsonMarshable.get_members():
                continue
            value_instance = getattr(self, field)

            if value_instance and inspect.isclass(value) and issubclass(value, Model):
                obj[field] = value_instance.to_dict()
            else:
                obj[field] = value_instance

        return obj


class Model:

    def __init__(self, **kwargs):
        class_members = inspect.getmembers(self.__class__)
        class_members = dict(filter(lambda e: not e[0].startswith("__"), class_members))
        is_model_class = lambda e: inspect.isclass(e) and issubclass(e, Model)
        for name, value in kwargs.items():
            # If the atribute is defined in the model as a nested model then check
            # if the object given is an instance of that class.
            if is_model_class(class_members[name]) and not isinstance(value, Model):
                raise ValueError(
                    "Attribute '{}' is defined as {} type in {}. '{}' instance was given instead."
                    .format(
                        name,
                        class_members[name].__name__,
                        self.__class__.__name__,
                        value.__class__.__name__)
                )
            setattr(self, name, value)
        # Search for nested uninitialized models and set them to None.
        for name, member in inspect.getmembers(self):
            if is_model_class(member) and not name.startswith("__"):
                setattr(self, name, None)

class HttpInterface(metaclass=ABCMeta):

    @abstractmethod
    def get(self, url):
        pass

    @abstractmethod
    def post(self, url):
        pass

    @abstractmethod
    def delete(self, url):
        pass

    @abstractmethod
    def put(self, url):
        pass


class RequestAdapter(HttpInterface):

    def __init__(self):
        self.session = requests.Session()

    def get(self, url):
        return requests.get(url).json()

    def post(self, url):
        return requests.post(url).json()

    def delete(self, url):
        pass

    def put(self, url):
        pass
