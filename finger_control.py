#!/usr/bin/env python3
"""
Quick Individual Finger Control Script
Usage: python finger_control.py [finger] [angle]
Example: python finger_control.py thumb 90
         python finger_control.py index 45
"""

import sys
import time
from main import BionicHand, MockCommunicationChannel, SerialCommunicationChannel, IS_SERIAL_AVAILABLE

def quick_finger_control(finger_name=None, angle=None):
    """Quick function to control a single finger."""
    
    # Setup communication (simulation mode for now)
    comm_channel = MockCommunicationChannel(port="SIM_PORT", baud_rate=9600)
    hand = BionicHand(channel=comm_channel)
    
    finger_map = {
        "thumb": 0, "t": 0,
        "index": 1, "i": 1, "pointer": 1,
        "middle": 2, "m": 2,
        "ring": 3, "r": 3,
        "pinky": 4, "p": 4, "little": 4
    }
    
    if finger_name and angle is not None:
        # Command line usage
        finger_name_lower = finger_name.lower()
        if finger_name_lower in finger_map:
            finger_index = finger_map[finger_name_lower]
            print(f"Moving {finger_name} (finger {finger_index}) to {angle}°")
            hand.move_finger(finger_index, angle)
        else:
            print(f"Unknown finger: {finger_name}")
            print("Valid fingers: thumb, index, middle, ring, pinky")
    else:
        # Interactive mode
        print("\n=== Quick Finger Control ===")
        print("Finger mapping:")
        print("0 = Thumb, 1 = Index, 2 = Middle, 3 = Ring, 4 = Pinky")
        print("\nCommands:")
        print("- Enter 'finger_name angle' (e.g., 'thumb 90')")
        print("- Enter 'finger_index angle' (e.g., '1 90')")
        print("- Enter 'q' to quit")
        
        while True:
            try:
                cmd = input("\nEnter command: ").strip()
                if cmd.lower() == 'q':
                    break
                
                parts = cmd.split()
                if len(parts) != 2:
                    print("Format: finger angle (e.g., 'thumb 90' or '1 90')")
                    continue
                
                finger_input, angle_str = parts
                angle = int(angle_str)
                
                if angle < 0 or angle > 180:
                    print("Angle must be between 0 and 180")
                    continue
                
                # Try as finger name first
                if finger_input.lower() in finger_map:
                    finger_index = finger_map[finger_input.lower()]
                    finger_name = finger_input
                # Try as finger index
                elif finger_input.isdigit() and 0 <= int(finger_input) <= 4:
                    finger_index = int(finger_input)
                    finger_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
                    finger_name = finger_names[finger_index]
                else:
                    print("Invalid finger. Use name (thumb/index/middle/ring/pinky) or index (0-4)")
                    continue
                
                print(f"Moving {finger_name} to {angle}°")
                hand.move_finger(finger_index, angle)
                
            except ValueError:
                print("Invalid angle. Please enter a number.")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
    
    hand.close_connection()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # Command line mode: python finger_control.py thumb 90
        finger_name = sys.argv[1]
        try:
            angle = int(sys.argv[2])
            quick_finger_control(finger_name, angle)
        except ValueError:
            print("Error: Angle must be a number")
            print("Usage: python finger_control.py [finger] [angle]")
    elif len(sys.argv) == 1:
        # Interactive mode
        quick_finger_control()
    else:
        print("Usage:")
        print("  python finger_control.py                    # Interactive mode")
        print("  python finger_control.py [finger] [angle]   # Direct control")
        print("Examples:")
        print("  python finger_control.py thumb 90")
        print("  python finger_control.py index 45")
        print("  python finger_control.py 2 180    # Middle finger to 180°")
