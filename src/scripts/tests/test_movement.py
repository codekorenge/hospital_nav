#!/usr/bin/env python3

import os
import sys

# Allow importing navigation.py from ../
SCRIPT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, SCRIPT_DIR)

import rclpy

from movement import (
    ArmController,
    fold_arm,
    handover_medication,
)


def main():

    rclpy.init()

    controller = ArmController()

    try:

        # ---------------------------------------------
        # Test 1: Fold
        # ---------------------------------------------

        print("\nTEST 1: Fold arm")

        if not fold_arm(controller):
            print("TEST FAILED: Fold")
            return

        print("TEST PASSED: Fold")

        # ---------------------------------------------
        # Test 2: Handover
        # ---------------------------------------------

        print("\nTEST 2: Handover pose")

        if not handover_medication(controller):
            print("TEST FAILED: Handover")
            return

        print("TEST PASSED: Handover")

        # ---------------------------------------------
        # Test 3: Fold again
        # ---------------------------------------------

        print("\nTEST 3: Fold arm again")

        if not fold_arm(controller):
            print("TEST FAILED: Final fold")
            return

        print("TEST PASSED: Final fold")

        print("\nALL MOVEMENT TESTS PASSED.")

    except KeyboardInterrupt:

        print("\nTEST INTERRUPTED.")

    finally:

        controller.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
