// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice
#include "vesc_msgs/msg/detail/vesc_cmd__rosidl_typesupport_fastrtps_cpp.hpp"
#include "vesc_msgs/msg/detail/vesc_cmd__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace vesc_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vesc_msgs
cdr_serialize(
  const vesc_msgs::msg::VescCmd & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: duty_cycle
  cdr << ros_message.duty_cycle;
  // Member: current
  cdr << ros_message.current;
  // Member: brake_current
  cdr << ros_message.brake_current;
  // Member: rpm
  cdr << ros_message.rpm;
  // Member: servo
  cdr << (ros_message.servo ? true : false);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vesc_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  vesc_msgs::msg::VescCmd & ros_message)
{
  // Member: duty_cycle
  cdr >> ros_message.duty_cycle;

  // Member: current
  cdr >> ros_message.current;

  // Member: brake_current
  cdr >> ros_message.brake_current;

  // Member: rpm
  cdr >> ros_message.rpm;

  // Member: servo
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.servo = tmp ? true : false;
  }

  return true;
}  // NOLINT(readability/fn_size)

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vesc_msgs
get_serialized_size(
  const vesc_msgs::msg::VescCmd & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: duty_cycle
  {
    size_t item_size = sizeof(ros_message.duty_cycle);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: current
  {
    size_t item_size = sizeof(ros_message.current);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: brake_current
  {
    size_t item_size = sizeof(ros_message.brake_current);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: rpm
  {
    size_t item_size = sizeof(ros_message.rpm);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: servo
  {
    size_t item_size = sizeof(ros_message.servo);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_vesc_msgs
max_serialized_size_VescCmd(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;


  // Member: duty_cycle
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: current
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: brake_current
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: rpm
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint32_t);
    current_alignment += array_size * sizeof(uint32_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint32_t));
  }

  // Member: servo
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = vesc_msgs::msg::VescCmd;
    is_plain =
      (
      offsetof(DataType, servo) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static bool _VescCmd__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const vesc_msgs::msg::VescCmd *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _VescCmd__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<vesc_msgs::msg::VescCmd *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _VescCmd__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const vesc_msgs::msg::VescCmd *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _VescCmd__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_VescCmd(full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}

static message_type_support_callbacks_t _VescCmd__callbacks = {
  "vesc_msgs::msg",
  "VescCmd",
  _VescCmd__cdr_serialize,
  _VescCmd__cdr_deserialize,
  _VescCmd__get_serialized_size,
  _VescCmd__max_serialized_size
};

static rosidl_message_type_support_t _VescCmd__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_VescCmd__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace vesc_msgs

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_vesc_msgs
const rosidl_message_type_support_t *
get_message_type_support_handle<vesc_msgs::msg::VescCmd>()
{
  return &vesc_msgs::msg::typesupport_fastrtps_cpp::_VescCmd__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, vesc_msgs, msg, VescCmd)() {
  return &vesc_msgs::msg::typesupport_fastrtps_cpp::_VescCmd__handle;
}

#ifdef __cplusplus
}
#endif
