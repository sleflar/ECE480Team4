// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from vesc_msgs:msg/VescCmd.idl
// generated code does not contain a copyright notice

#ifndef VESC_MSGS__MSG__DETAIL__VESC_CMD__STRUCT_HPP_
#define VESC_MSGS__MSG__DETAIL__VESC_CMD__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__vesc_msgs__msg__VescCmd __attribute__((deprecated))
#else
# define DEPRECATED__vesc_msgs__msg__VescCmd __declspec(deprecated)
#endif

namespace vesc_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VescCmd_
{
  using Type = VescCmd_<ContainerAllocator>;

  explicit VescCmd_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->duty_cycle = 0.0f;
      this->current = 0.0f;
      this->brake_current = 0.0f;
      this->rpm = 0.0f;
      this->servo = false;
    }
  }

  explicit VescCmd_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->duty_cycle = 0.0f;
      this->current = 0.0f;
      this->brake_current = 0.0f;
      this->rpm = 0.0f;
      this->servo = false;
    }
  }

  // field types and members
  using _duty_cycle_type =
    float;
  _duty_cycle_type duty_cycle;
  using _current_type =
    float;
  _current_type current;
  using _brake_current_type =
    float;
  _brake_current_type brake_current;
  using _rpm_type =
    float;
  _rpm_type rpm;
  using _servo_type =
    bool;
  _servo_type servo;

  // setters for named parameter idiom
  Type & set__duty_cycle(
    const float & _arg)
  {
    this->duty_cycle = _arg;
    return *this;
  }
  Type & set__current(
    const float & _arg)
  {
    this->current = _arg;
    return *this;
  }
  Type & set__brake_current(
    const float & _arg)
  {
    this->brake_current = _arg;
    return *this;
  }
  Type & set__rpm(
    const float & _arg)
  {
    this->rpm = _arg;
    return *this;
  }
  Type & set__servo(
    const bool & _arg)
  {
    this->servo = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    vesc_msgs::msg::VescCmd_<ContainerAllocator> *;
  using ConstRawPtr =
    const vesc_msgs::msg::VescCmd_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      vesc_msgs::msg::VescCmd_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      vesc_msgs::msg::VescCmd_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__vesc_msgs__msg__VescCmd
    std::shared_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__vesc_msgs__msg__VescCmd
    std::shared_ptr<vesc_msgs::msg::VescCmd_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VescCmd_ & other) const
  {
    if (this->duty_cycle != other.duty_cycle) {
      return false;
    }
    if (this->current != other.current) {
      return false;
    }
    if (this->brake_current != other.brake_current) {
      return false;
    }
    if (this->rpm != other.rpm) {
      return false;
    }
    if (this->servo != other.servo) {
      return false;
    }
    return true;
  }
  bool operator!=(const VescCmd_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VescCmd_

// alias to use template instance with default allocator
using VescCmd =
  vesc_msgs::msg::VescCmd_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace vesc_msgs

#endif  // VESC_MSGS__MSG__DETAIL__VESC_CMD__STRUCT_HPP_
