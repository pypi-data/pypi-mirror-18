# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
import abc

import six

from ._converter import (
    NopConverter,
    StringConverter,
    IntegerConverter,
    FloatConverter,
    BoolConverter,
    DateTimeConverter
)
from ._type_checker import (
    NoneTypeChecker,
    StringTypeChecker,
    IntegerTypeChecker,
    FloatTypeChecker,
    BoolTypeChecker,
    DateTimeTypeChecker,
    InfinityChecker,
    NanChecker
)


@six.add_metaclass(abc.ABCMeta)
class TypeFactoryInterface(object):
    """
    Abstract factory class of type converter.
    """

    @abc.abstractmethod
    def create_type_checker(self):  # pragma: no cover
        pass

    @abc.abstractmethod
    def create_type_converter(self):  # pragma: no cover
        pass


class BaseTypeFactory(TypeFactoryInterface):
    __slots__ = ("_data", "_is_strict")

    def __init__(self, data, is_strict):
        self._data = data
        self._is_strict = is_strict


class NoneTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return NoneTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return NopConverter(self._data)


class StringTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return StringTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return StringConverter(self._data)


class IntegerTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return IntegerTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return IntegerConverter(self._data)


class FloatTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return FloatTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return FloatConverter(self._data)


class DateTimeTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return DateTimeTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return DateTimeConverter(self._data)


class BoolTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return BoolTypeChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return BoolConverter(self._data)


class InfinityTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return InfinityChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return FloatConverter(self._data)


class NanTypeFactory(BaseTypeFactory):

    def create_type_checker(self):
        return NanChecker(self._data, self._is_strict)

    def create_type_converter(self):
        return FloatConverter(self._data)
