from __future__ import absolute_import

from enum import Enum as BaseEnum, EnumMeta as BaseEnumMeta, unique  # noqa: F401


########################################
# Base Enum classes
########################################

class EnumMeta(BaseEnumMeta):
    """ Custom Enum metaclass to create Enums with members that have a value, label, and metadata. """
    def __new__(metacls, cls, bases, classdict):
        obj = BaseEnumMeta.__new__(metacls, cls, bases, classdict)
        if obj._value2member_map_:
            # Update the Enum's internal mapping of value --> Enum member
            new_value2member_map = {}
            for value, member in obj._value2member_map_.items():
                # Check if the Enum member is declared with additional data, like a label and metadata
                if isinstance(value, (list, tuple)) and len(value) > 1:
                    # Set the Enum member's internal attributes to the actual value, label, and metadata
                    member._value_ = value[0]
                    member._label_ = value[1]
                    member._metadata_ = value[2:] or None
                    new_value2member_map[value[0]] = member
                else:
                    # Add a label to the Enum member that is derived from its name
                    member._label_ = member.name.replace('_', ' ').title()
                    new_value2member_map[value] = member
            obj._value2member_map_ = new_value2member_map

        return obj


class Enum(BaseEnum):
    __metaclass__ = EnumMeta

    @property
    def label(self):
        """ A descriptive string label for this Enum member. """
        return self._label_

    @property
    def metadata(self):
        """ The collection of metadata associated with this Enum member (exclusive of its value and label). """
        return self._metadata_

    @classmethod
    def choices(cls):
        """ A list of tuples: (value, label). Can be used to populate a drop-down for example. """
        return tuple((m.value, m.label) for m in cls)

    def add_alias(self, value):
        """ Associate another value with this Enum member. """
        enum_member_cls = self.__objclass__
        if value in enum_member_cls._value2member_map_:
            raise ValueError("{} already exists as a {} value".format(value, enum_member_cls.__name__))
        enum_member_cls._value2member_map_[value] = self


class ValueComparableEnum(Enum):
    """ An Enum where members are comparable to each other by value. """
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ >= other._value_
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ > other._value_
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ <= other._value_
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ < other._value_
        return NotImplemented


class OrderComparableEnum(Enum):
    """
    An Enum where members are comparable to each other by their order.

    Note: Unordered Enums are not compared predictably.
          Also, any non-unique Enum members (aliases) will share the same ordering value.
    """
    @classmethod
    def _order(cls, member):
        return cls._member_names_.index(member.name)

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self._order(self) >= self._order(other)
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self._order(self) > self._order(other)
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self._order(self) <= self._order(other)
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._order(self) < self._order(other)
        return NotImplemented


########################################
# Enum decorators
########################################

def _reorder_enum(enumeration, by_member, reverse=False):
    enumeration._member_names_ = [e.name for e in sorted(
        enumeration._value2member_map_.values(), key=lambda x: getattr(x, by_member), reverse=reverse)]


def order_by_name(enumeration):
    """ Decorate an Enum with this to have its members ordered by name."""
    _reorder_enum(enumeration, 'name')
    return enumeration


def order_by_name_reversed(enumeration):
    """ Decorate an Enum with this to have its members reverse ordered by name."""
    _reorder_enum(enumeration, 'name', reverse=True)
    return enumeration


def order_by_value(enumeration):
    """ Decorate an Enum with this to have its members ordered by value."""
    _reorder_enum(enumeration, 'value')
    return enumeration


def order_by_value_reversed(enumeration):
    """ Decorate an Enum with this to have its members reverse ordered by value."""
    _reorder_enum(enumeration, 'value', reverse=True)
    return enumeration
