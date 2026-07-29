#!/usr/bin/env python3

import argparse

import rclpy

from navigation import create_navigator, navigate_to
from movement import ArmController, execute_action


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="TIAGo navigation + manipulation action"
    )

    parser.add_argument(
        "--nav",
        required=True,
        help="Navigation goal: x,y,yaw"
    )

    parser.add_argument(
        "--action",
        required=True,
        choices=[
            "fold",
            "handover",
        ],
        help="Action to execute after navigation"
    )

    return parser.parse_args()


def parse_nav(value):
    """Convert x,y,yaw string into floats."""

    values = value.split(",")

    if len(values) != 3:
        raise ValueError(
            "Navigation must be specified as x,y,yaw"
        )

    return [float(v) for v in values]


def main():

    args = parse_arguments()

    try:
        x, y, yaw = parse_nav(args.nav)

    except ValueError as error:
        print(f"Error: {error}")
        return

    rclpy.init()

    navigator = create_navigator()
    arm_controller = ArmController()

    try:

        # ---------------------------------------------
        # Step 1: Navigate
        # ---------------------------------------------

        navigation_success = navigate_to(
            navigator,
            x,
            y,
            yaw
        )

        if not navigation_success:
            print(
                "\nNavigation failed."
                "\nAction will NOT be executed."
            )
            return

        # ---------------------------------------------
        # Step 2: Perform action
        # ---------------------------------------------

        print(
            f"\nExecuting action: {args.action}"
        )

        action_success = execute_action(
            arm_controller,
            args.action
        )

        if action_success:
            print(
                f"\nAction '{args.action}' completed."
            )
        else:
            print(
                f"\nAction '{args.action}' failed."
            )

    except KeyboardInterrupt:

        print("\nOperation interrupted.")
        navigator.cancelTask()

    finally:

        navigator.destroyNode()
        arm_controller.destroy_node()

        rclpy.shutdown()


if __name__ == "__main__":
    main()
