// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice
#include "vesc_msgs/msg/detail/vesc_cmd__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
vesc_msgs__msg__VescCmd__init(vesc_msgs__msg__VescCmd * msg)
{
  if (!msg) {
    return false;
  }
  // duty_cycle
  // current
  // brake_current
  // rpm
  // servo
  return true;
}

void
vesc_msgs__msg__VescCmd__fini(vesc_msgs__msg__VescCmd * msg)
{
  if (!msg) {
    return;
  }
  // duty_cycle
  // current
  // brake_current
  // rpm
  // servo
}

bool
vesc_msgs__msg__VescCmd__are_equal(const vesc_msgs__msg__VescCmd * lhs, const vesc_msgs__msg__VescCmd * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // duty_cycle
  if (lhs->duty_cycle != rhs->duty_cycle) {
    return false;
  }
  // current
  if (lhs->current != rhs->current) {
    return false;
  }
  // brake_current
  if (lhs->brake_current != rhs->brake_current) {
    return false;
  }
  // rpm
  if (lhs->rpm != rhs->rpm) {
    return false;
  }
  // servo
  if (lhs->servo != rhs->servo) {
    return false;
  }
  return true;
}

bool
vesc_msgs__msg__VescCmd__copy(
  const vesc_msgs__msg__VescCmd * input,
  vesc_msgs__msg__VescCmd * output)
{
  if (!input || !output) {
    return false;
  }
  // duty_cycle
  output->duty_cycle = input->duty_cycle;
  // current
  output->current = input->current;
  // brake_current
  output->brake_current = input->brake_current;
  // rpm
  output->rpm = input->rpm;
  // servo
  output->servo = input->servo;
  return true;
}

vesc_msgs__msg__VescCmd *
vesc_msgs__msg__VescCmd__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vesc_msgs__msg__VescCmd * msg = (vesc_msgs__msg__VescCmd *)allocator.allocate(sizeof(vesc_msgs__msg__VescCmd), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(vesc_msgs__msg__VescCmd));
  bool success = vesc_msgs__msg__VescCmd__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
vesc_msgs__msg__VescCmd__destroy(vesc_msgs__msg__VescCmd * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    vesc_msgs__msg__VescCmd__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
vesc_msgs__msg__VescCmd__Sequence__init(vesc_msgs__msg__VescCmd__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vesc_msgs__msg__VescCmd * data = NULL;

  if (size) {
    data = (vesc_msgs__msg__VescCmd *)allocator.zero_allocate(size, sizeof(vesc_msgs__msg__VescCmd), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = vesc_msgs__msg__VescCmd__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        vesc_msgs__msg__VescCmd__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
vesc_msgs__msg__VescCmd__Sequence__fini(vesc_msgs__msg__VescCmd__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      vesc_msgs__msg__VescCmd__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

vesc_msgs__msg__VescCmd__Sequence *
vesc_msgs__msg__VescCmd__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  vesc_msgs__msg__VescCmd__Sequence * array = (vesc_msgs__msg__VescCmd__Sequence *)allocator.allocate(sizeof(vesc_msgs__msg__VescCmd__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = vesc_msgs__msg__VescCmd__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
vesc_msgs__msg__VescCmd__Sequence__destroy(vesc_msgs__msg__VescCmd__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    vesc_msgs__msg__VescCmd__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
vesc_msgs__msg__VescCmd__Sequence__are_equal(const vesc_msgs__msg__VescCmd__Sequence * lhs, const vesc_msgs__msg__VescCmd__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!vesc_msgs__msg__VescCmd__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
vesc_msgs__msg__VescCmd__Sequence__copy(
  const vesc_msgs__msg__VescCmd__Sequence * input,
  vesc_msgs__msg__VescCmd__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(vesc_msgs__msg__VescCmd);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    vesc_msgs__msg__VescCmd * data =
      (vesc_msgs__msg__VescCmd *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!vesc_msgs__msg__VescCmd__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          vesc_msgs__msg__VescCmd__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!vesc_msgs__msg__VescCmd__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
