# generated from rosidl_generator_py/resource/_idl.py.em
# with input from vesc_msgs:msg/VescCmd.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_VescCmd(type):
    """Metaclass of message 'VescCmd'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('vesc_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'vesc_msgs.msg.VescCmd')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__vesc_cmd
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__vesc_cmd
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__vesc_cmd
            cls._TYPE_SUPPORT = module.type_support_msg__msg__vesc_cmd
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__vesc_cmd

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class VescCmd(metaclass=Metaclass_VescCmd):
    """Message class 'VescCmd'."""

    __slots__ = [
        '_duty_cycle',
        '_current',
        '_brake_current',
        '_rpm',
        '_servo',
    ]

    _fields_and_field_types = {
        'duty_cycle': 'float',
        'current': 'float',
        'brake_current': 'float',
        'rpm': 'float',
        'servo': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.duty_cycle = kwargs.get('duty_cycle', float())
        self.current = kwargs.get('current', float())
        self.brake_current = kwargs.get('brake_current', float())
        self.rpm = kwargs.get('rpm', float())
        self.servo = kwargs.get('servo', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.duty_cycle != other.duty_cycle:
            return False
        if self.current != other.current:
            return False
        if self.brake_current != other.brake_current:
            return False
        if self.rpm != other.rpm:
            return False
        if self.servo != other.servo:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def duty_cycle(self):
        """Message field 'duty_cycle'."""
        return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'duty_cycle' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'duty_cycle' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._duty_cycle = value

    @builtins.property
    def current(self):
        """Message field 'current'."""
        return self._current

    @current.setter
    def current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._current = value

    @builtins.property
    def brake_current(self):
        """Message field 'brake_current'."""
        return self._brake_current

    @brake_current.setter
    def brake_current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'brake_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'brake_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._brake_current = value

    @builtins.property
    def rpm(self):
        """Message field 'rpm'."""
        return self._rpm

    @rpm.setter
    def rpm(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'rpm' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'rpm' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._rpm = value

    @builtins.property
    def servo(self):
        """Message field 'servo'."""
        return self._servo

    @servo.setter
    def servo(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'servo' field must be of type 'bool'"
        self._servo = value
