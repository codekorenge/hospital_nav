#!/usr/bin/env python3

import os
import sys

# Allow importing navigation.py from ../
SCRIPT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, SCRIPT_DIR)

import rclpy

from navigation import create_navigator, navigate_to


def main():

    if len(sys.argv) != 4:
        print(
            "Usage:\n"
            "  python3 test_navigation.py x y yaw\n\n"
            "Example:\n"
            "  python3 test_navigation.py 0.5 5.5 0"
        )
        return

    x = float(sys.argv[1])
    y = float(sys.argv[2])
    yaw = float(sys.argv[3])

    rclpy.init()

    navigator = create_navigator()

    try:

        print(
            f"\nTEST: Navigate to "
            f"({x}, {y}, {yaw})"
        )

        success = navigate_to(
            navigator,
            x,
            y,
            yaw
        )

        if success:
            print("\nTEST PASSED: Navigation succeeded.")
        else:
            print("\nTEST FAILED: Navigation failed.")

    except KeyboardInterrupt:
        print("\nTEST INTERRUPTED.")
        navigator.cancelTask()

    finally:
        navigator.destroyNode()
        rclpy.shutdown()


if __name__ == "__main__":
    main()