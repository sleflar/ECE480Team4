// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice

#ifndef VESC_MSGS__MSG__DETAIL__VESC_CMD__TRAITS_HPP_
#define VESC_MSGS__MSG__DETAIL__VESC_CMD__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "vesc_msgs/msg/detail/vesc_cmd__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace vesc_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const VescCmd & msg,
  std::ostream & out)
{
  out << "{";
  // member: duty_cycle
  {
    out << "duty_cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.duty_cycle, out);
    out << ", ";
  }

  // member: current
  {
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << ", ";
  }

  // member: brake_current
  {
    out << "brake_current: ";
    rosidl_generator_traits::value_to_yaml(msg.brake_current, out);
    out << ", ";
  }

  // member: rpm
  {
    out << "rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.rpm, out);
    out << ", ";
  }

  // member: servo
  {
    out << "servo: ";
    rosidl_generator_traits::value_to_yaml(msg.servo, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const VescCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: duty_cycle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "duty_cycle: ";
    rosidl_generator_traits::value_to_yaml(msg.duty_cycle, out);
    out << "\n";
  }

  // member: current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "current: ";
    rosidl_generator_traits::value_to_yaml(msg.current, out);
    out << "\n";
  }

  // member: brake_current
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "brake_current: ";
    rosidl_generator_traits::value_to_yaml(msg.brake_current, out);
    out << "\n";
  }

  // member: rpm
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "rpm: ";
    rosidl_generator_traits::value_to_yaml(msg.rpm, out);
    out << "\n";
  }

  // member: servo
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "servo: ";
    rosidl_generator_traits::value_to_yaml(msg.servo, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const VescCmd & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace vesc_msgs

namespace rosidl_generator_traits
{

[[deprecated("use vesc_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const vesc_msgs::msg::VescCmd & msg,
  std::ostream & out, size_t indentation = 0)
{
  vesc_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use vesc_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const vesc_msgs::msg::VescCmd & msg)
{
  return vesc_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<vesc_msgs::msg::VescCmd>()
{
  return "vesc_msgs::msg::VescCmd";
}

template<>
inline const char * name<vesc_msgs::msg::VescCmd>()
{
  return "vesc_msgs/msg/VescCmd";
}

template<>
struct has_fixed_size<vesc_msgs::msg::VescCmd>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<vesc_msgs::msg::VescCmd>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<vesc_msgs::msg::VescCmd>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // VESC_MSGS__MSG__DETAIL__VESC_CMD__TRAITS_HPP_
