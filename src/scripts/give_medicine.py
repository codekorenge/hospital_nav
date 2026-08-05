#!/usr/bin/env python3

import argparse
import subprocess
import sys
import time

"""
This script uses the med_action.py script to deliver medicine to a specified patient.
"""

# Patient locations
PATIENTS = {
    "patient01": (0.6, 5.6, 0.0),
    "patient02": (-0.6, 5.6, 3.14),
    "patient03": (5.6, -0.6, 0.0),
}


# Run med_action.py
def run_med_action(x, y, yaw, action):
    """Run med_action.py with the specified navigation and action."""

    command = [
        "./med_action.py",
        f"--nav={x},{y},{yaw}",
        "--action",
        action,
    ]

    print(f"\nExecuting: {' '.join(command)}\n")

    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"\nmed_action.py failed " f"with return code {result.returncode}")
        return False

    return True


# Give medicine
def give_medicine(patient_id):
    """Navigate to patient, hand over medicine, then return home."""

    x, y, yaw = PATIENTS[patient_id]

    print(f"\nPatient: {patient_id}" f"\nLocation: x={x}, y={y}, yaw={yaw}")

    # 1. Navigate to patient + handover
    if not run_med_action(x, y, yaw, "handover"):
        return False

    # 2. Fold arm
    if not run_med_action(x, y, yaw, "fold"):
        return False

    # 3. Return home + fold
    if not run_med_action(0.0, 0.0, 0.0, "fold"):
        return False

    print(f"\nMedicine delivery to {patient_id} completed.")

    return True


# Main
def main():

    parser = argparse.ArgumentParser(description="Deliver medicine to a patient.")

    parser.add_argument(
        "patient", choices=PATIENTS.keys(), help="Patient to deliver medicine to."
    )

    args = parser.parse_args()

    # Capture start time.
    start_time = time.perf_counter()

    success = give_medicine(args.patient)

    # Calculate elapsed time and print
    execution_time = time.perf_counter() - start_time
    print(f"Navigation took {execution_time:.2f} seconds.") 

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
