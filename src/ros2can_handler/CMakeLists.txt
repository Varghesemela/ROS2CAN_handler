cmake_minimum_required(VERSION 3.8)
project(ros2can_handler)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(ros2can_handler src/ros2can_handler.cpp)
ament_target_dependencies(ros2can_handler rclcpp example_interfaces)

install(TARGETS
  ros2can_handler
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
