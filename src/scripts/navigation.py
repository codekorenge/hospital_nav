#!/usr/bin/env python3

import math

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator


def create_goal(navigator, x, y, yaw):
    """Create a Nav2 goal pose in the map frame."""

    goal = PoseStamped()

    goal.header.frame_id = "map"
    goal.header.stamp = navigator.get_clock().now().to_msg()

    goal.pose.position.x = x
    goal.pose.position.y = y

    # Yaw -> quaternion
    goal.pose.orientation.z = math.sin(yaw / 2.0)
    goal.pose.orientation.w = math.cos(yaw / 2.0)

    return goal


def navigate_to(navigator, x, y, yaw):
    """Navigate to (x, y, yaw).

    Returns True when Nav2 reports success.
    """

    print(f"Navigation goal: x={x}, y={y}, yaw={yaw}")

    goal = create_goal(
        navigator,
        x,
        y,
        yaw
    )

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

    return str(result) == "TaskResult.SUCCEEDED"


def create_navigator():
    """Create and activate the Nav2 navigator."""

    navigator = BasicNavigator()

    print("Waiting for Nav2...")
    navigator.waitUntilNav2Active()

    return navigator
