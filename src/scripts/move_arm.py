#!/usr/bin/env python3

import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint


ARM_JOINTS = [
    "arm_1_joint",
    "arm_2_joint",
    "arm_3_joint",
    "arm_4_joint",
    "arm_5_joint",
    "arm_6_joint",
    "arm_7_joint",
]


# ---------------------------------------------------------
# Named arm poses
# ---------------------------------------------------------

FOLDED_POSE = [
    0.0,    # arm_1
    0.8,    # arm_2
    -1.5,   # arm_3
    1.8,    # arm_4
    0.0,    # arm_5
    0.0,    # arm_6
    0.0,    # arm_7
]

MED_HANDOVER_POSE = [
    0.0,    # arm_1
    0.4,    # arm_2
    -1.2,   # arm_3
    1.2,    # arm_4
    0.0,    # arm_5
    0.8,    # arm_6
    0.0,    # arm_7
]


class ArmController(Node):

    def __init__(self):
        super().__init__("tiago_arm_controller")

        self.client = ActionClient(
            self,
            FollowJointTrajectory,
            "/arm_controller/follow_joint_trajectory",
        )

    def move_to(self, positions, duration=5.0):
        """Move the arm to a joint configuration."""

        if len(positions) != len(ARM_JOINTS):
            raise ValueError("Expected 7 joint positions.")

        goal = FollowJointTrajectory.Goal()

        goal.trajectory.joint_names = ARM_JOINTS

        point = JointTrajectoryPoint()
        point.positions = positions
        point.time_from_start.sec = int(duration)

        goal.trajectory.points.append(point)

        self.get_logger().info(
            f"Moving arm to: {positions}"
        )

        self.client.wait_for_server()

        future = self.client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, future)

        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error(
                "Arm trajectory rejected."
            )
            return False

        self.get_logger().info(
            "Arm trajectory accepted."
        )

        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(
            self,
            result_future
        )

        result = result_future.result().result

        self.get_logger().info(
            f"Arm motion completed with error code: "
            f"{result.error_code}"
        )

        return result.error_code == 0


def fold_arm(controller):
    """Move TIAGo's arm to the folded pose."""

    return controller.move_to(FOLDED_POSE)

def handover_medication(controller):
    """Move TIAGo's arm into a medication handover pose."""
    return controller.move_to(MED_HANDOVER_POSE)


def main():

    if len(sys.argv) != 2:
        print(
            "Usage:\n"
            "  python3 move_arm.py fold"
        )
        return

    command = sys.argv[1].lower()

    rclpy.init()

    controller = ArmController()

    try:

        if command == "fold":
            fold_arm(controller)
        elif command == "handover":
            handover_medication(controller)
        else:
            print(f"Unknown command: {command}")
            print("Available commands: fold, handover")

    except KeyboardInterrupt:
        print("\nMotion interrupted.")

    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
