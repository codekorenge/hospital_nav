#!/usr/bin/env python3

import sys
import math

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator


def parse_goal(args):
    """Parse x, y and yaw from command-line arguments."""

    if len(args) != 3:
        raise ValueError(
            "Usage: python3 go_to_goal.py x=1 y=6 yaw=0"
        )

    values = {}

    for arg in args:
        name, value = arg.split("=")
        values[name] = float(value)

    if not {"x", "y", "yaw"} <= values.keys():
        raise ValueError(
            "Required arguments: x, y and yaw"
        )

    return values["x"], values["y"], values["yaw"]


def create_goal(navigator, x, y, yaw):
    """Create a Nav2 PoseStamped goal in the map frame."""

    goal = PoseStamped()

    goal.header.frame_id = "map"
    goal.header.stamp = navigator.get_clock().now().to_msg()

    goal.pose.position.x = x
    goal.pose.position.y = y

    # Convert yaw to quaternion.
    goal.pose.orientation.z = math.sin(yaw / 2.0)
    goal.pose.orientation.w = math.cos(yaw / 2.0)

    return goal


def navigate_to(navigator, x, y, yaw):
    """Navigate TIAGo to the requested pose."""

    print(f"Navigating to: x={x}, y={y}, yaw={yaw}")

    goal = create_goal(navigator, x, y, yaw)

    navigator.goToPose(goal)

    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()

        if feedback is not None:
            print(
                f"Distance remaining: "
                f"{feedback.distance_remaining:.2f} m"
            )

    result = navigator.getResult()

    print(f"Navigation result: {result}")

    return result


def main():
    try:
        x, y, yaw = parse_goal(sys.argv[1:])
    except (ValueError, IndexError) as error:
        print(f"Error: {error}")
        return

    rclpy.init()

    navigator = BasicNavigator()

    try:
        print("Waiting for Nav2...")
        navigator.waitUntilNav2Active()

        navigate_to(navigator, x, y, yaw)

    except KeyboardInterrupt:
        print("\nNavigation interrupted.")
        navigator.cancelTask()

    finally:
        navigator.destroyNode()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
