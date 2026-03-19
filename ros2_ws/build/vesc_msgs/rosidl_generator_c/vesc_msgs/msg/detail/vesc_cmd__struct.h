// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice

#ifndef VESC_MSGS__MSG__DETAIL__VESC_CMD__STRUCT_H_
#define VESC_MSGS__MSG__DETAIL__VESC_CMD__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/VescCmd in the package vesc_msgs.
typedef struct vesc_msgs__msg__VescCmd
{
  float duty_cycle;
  float current;
  float brake_current;
  float rpm;
  bool servo;
} vesc_msgs__msg__VescCmd;

// Struct for a sequence of vesc_msgs__msg__VescCmd.
typedef struct vesc_msgs__msg__VescCmd__Sequence
{
  vesc_msgs__msg__VescCmd * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} vesc_msgs__msg__VescCmd__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // VESC_MSGS__MSG__DETAIL__VESC_CMD__STRUCT_H_
