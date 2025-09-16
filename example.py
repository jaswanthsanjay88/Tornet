#!/usr/bin/env python3
"""
Example usage of Tornet functionality
Demonstrates how to use the tornet module programmatically
"""

import sys
import os

# Add the parent directory to Python path to import tornet modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tornet import ma_ip, get_os_type, is_tor_installed
from banner import print_banner
from utils import check_system_requirements, print_system_info


def main():
    """Demonstrate Tornet functionality"""
    print("🧅 Tornet Example Usage\n")
    
    # Display banner
    print_banner()
    
    # Show system information
    print("\n📋 System Information:")
    print_system_info()
    
    # Check if Tor is installed
    print(f"\n🔍 Tor Installation Status: {'✅ Installed' if is_tor_installed() else '❌ Not Found'}")
    
    # Display current IP
    print("\n🌐 IP Address Information:")
    current_ip = ma_ip()
    if current_ip:
        print(f"Current IP: {current_ip}")
    else:
        print("Could not retrieve IP address")
    
    # Show OS type
    print(f"Operating System: {get_os_type()}")
    
    print("\n✨ Example completed!")
    print("To start IP rotation, run: python tornet.py --interval 60 --count 5")


if __name__ == "__main__":
    main()