// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "vesc_msgs/msg/detail/vesc_cmd__struct.h"
#include "vesc_msgs/msg/detail/vesc_cmd__functions.h"


ROSIDL_GENERATOR_C_EXPORT
bool vesc_msgs__msg__vesc_cmd__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[32];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("vesc_msgs.msg._vesc_cmd.VescCmd", full_classname_dest, 31) == 0);
  }
  vesc_msgs__msg__VescCmd * ros_message = _ros_message;
  {  // duty_cycle
    PyObject * field = PyObject_GetAttrString(_pymsg, "duty_cycle");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->duty_cycle = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // current
    PyObject * field = PyObject_GetAttrString(_pymsg, "current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // brake_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "brake_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->brake_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // rpm
    PyObject * field = PyObject_GetAttrString(_pymsg, "rpm");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->rpm = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // servo
    PyObject * field = PyObject_GetAttrString(_pymsg, "servo");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->servo = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * vesc_msgs__msg__vesc_cmd__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of VescCmd */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("vesc_msgs.msg._vesc_cmd");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "VescCmd");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  vesc_msgs__msg__VescCmd * ros_message = (vesc_msgs__msg__VescCmd *)raw_ros_message;
  {  // duty_cycle
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->duty_cycle);
    {
      int rc = PyObject_SetAttrString(_pymessage, "duty_cycle", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // brake_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->brake_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "brake_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // rpm
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->rpm);
    {
      int rc = PyObject_SetAttrString(_pymessage, "rpm", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // servo
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->servo ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "servo", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
