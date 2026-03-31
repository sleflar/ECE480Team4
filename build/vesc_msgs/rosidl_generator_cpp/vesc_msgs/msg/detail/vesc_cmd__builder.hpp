// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice

#ifndef VESC_MSGS__MSG__DETAIL__VESC_CMD__BUILDER_HPP_
#define VESC_MSGS__MSG__DETAIL__VESC_CMD__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "vesc_msgs/msg/detail/vesc_cmd__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace vesc_msgs
{

namespace msg
{

namespace builder
{

class Init_VescCmd_servo
{
public:
  explicit Init_VescCmd_servo(::vesc_msgs::msg::VescCmd & msg)
  : msg_(msg)
  {}
  ::vesc_msgs::msg::VescCmd servo(::vesc_msgs::msg::VescCmd::_servo_type arg)
  {
    msg_.servo = std::move(arg);
    return std::move(msg_);
  }

private:
  ::vesc_msgs::msg::VescCmd msg_;
};

class Init_VescCmd_rpm
{
public:
  explicit Init_VescCmd_rpm(::vesc_msgs::msg::VescCmd & msg)
  : msg_(msg)
  {}
  Init_VescCmd_servo rpm(::vesc_msgs::msg::VescCmd::_rpm_type arg)
  {
    msg_.rpm = std::move(arg);
    return Init_VescCmd_servo(msg_);
  }

private:
  ::vesc_msgs::msg::VescCmd msg_;
};

class Init_VescCmd_brake_current
{
public:
  explicit Init_VescCmd_brake_current(::vesc_msgs::msg::VescCmd & msg)
  : msg_(msg)
  {}
  Init_VescCmd_rpm brake_current(::vesc_msgs::msg::VescCmd::_brake_current_type arg)
  {
    msg_.brake_current = std::move(arg);
    return Init_VescCmd_rpm(msg_);
  }

private:
  ::vesc_msgs::msg::VescCmd msg_;
};

class Init_VescCmd_current
{
public:
  explicit Init_VescCmd_current(::vesc_msgs::msg::VescCmd & msg)
  : msg_(msg)
  {}
  Init_VescCmd_brake_current current(::vesc_msgs::msg::VescCmd::_current_type arg)
  {
    msg_.current = std::move(arg);
    return Init_VescCmd_brake_current(msg_);
  }

private:
  ::vesc_msgs::msg::VescCmd msg_;
};

class Init_VescCmd_duty_cycle
{
public:
  Init_VescCmd_duty_cycle()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VescCmd_current duty_cycle(::vesc_msgs::msg::VescCmd::_duty_cycle_type arg)
  {
    msg_.duty_cycle = std::move(arg);
    return Init_VescCmd_current(msg_);
  }

private:
  ::vesc_msgs::msg::VescCmd msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::vesc_msgs::msg::VescCmd>()
{
  return vesc_msgs::msg::builder::Init_VescCmd_duty_cycle();
}

}  // namespace vesc_msgs

#endif  // VESC_MSGS__MSG__DETAIL__VESC_CMD__BUILDER_HPP_
