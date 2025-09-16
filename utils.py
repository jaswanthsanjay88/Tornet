#!/usr/bin/env python3
"""
Utility functions for tornet - Tor network automation tool
Handles installation and system management tasks
"""

import os
import sys
import subprocess
import platform
import shutil

# ANSI color codes for consistent output
GREEN = "\033[92m"
RED = "\033[91m"
WHITE = "\033[97m"
RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[93m"


def run_command(command, description=None, check_success=True):
    """
    Execute a shell command with proper error handling.
    
    Args:
        command (str): Command to execute
        description (str): Description of what the command does
        check_success (bool): Whether to check for successful execution
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    if description:
        print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} {description}{RESET}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check_success and result.returncode != 0:
            print(f"{WHITE} [{RED}!{WHITE}] {RED}Command failed: {command}{RESET}")
            print(f"{WHITE} [{RED}!{WHITE}] {RED}Error: {result.stderr.strip()}{RESET}")
            return False
        return True
    except Exception as e:
        print(f"{WHITE} [{RED}!{WHITE}] {RED}Exception running command '{command}': {e}{RESET}")
        return False


def is_command_available(command):
    """
    Check if a command is available in the system PATH.
    
    Args:
        command (str): Command name to check
        
    Returns:
        bool: True if command is available, False otherwise
    """
    return shutil.which(command) is not None


def get_os_info():
    """
    Get detailed OS information.
    
    Returns:
        dict: Dictionary containing OS details
    """
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor()
    }


def install_pip():
    """
    Ensure pip is installed and available.
    """
    print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} Checking pip installation...{RESET}")
    
    if is_command_available('pip') or is_command_available('pip3'):
        print(f"{WHITE} [{GREEN}+{WHITE}]{GREEN} pip is already installed.{RESET}")
        return True
    
    os_type = platform.system()
    
    if os_type == "Linux":
        # Try different package managers
        if is_command_available('apt'):
            return run_command("sudo apt update && sudo apt install -y python3-pip", 
                             "Installing pip via apt")
        elif is_command_available('yum'):
            return run_command("sudo yum install -y python3-pip", 
                             "Installing pip via yum")
        elif is_command_available('dnf'):
            return run_command("sudo dnf install -y python3-pip", 
                             "Installing pip via dnf")
        elif is_command_available('pacman'):
            return run_command("sudo pacman -S --noconfirm python-pip", 
                             "Installing pip via pacman")
    elif os_type == "Darwin":  # macOS
        if is_command_available('brew'):
            return run_command("brew install python", "Installing pip via Homebrew")
        else:
            print(f"{WHITE} [{YELLOW}!{WHITE}] {YELLOW}Please install Homebrew first or install pip manually.{RESET}")
    elif os_type == "Windows":
        print(f"{WHITE} [{YELLOW}!{WHITE}] {YELLOW}On Windows, pip should come with Python. Please reinstall Python from python.org{RESET}")
    
    print(f"{WHITE} [{RED}!{WHITE}] {RED}Could not install pip automatically. Please install it manually.{RESET}")
    return False


def install_requests():
    """
    Install the requests library for HTTP operations.
    """
    print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} Checking requests library...{RESET}")
    
    try:
        import requests
        print(f"{WHITE} [{GREEN}+{WHITE}]{GREEN} requests library is already installed.{RESET}")
        return True
    except ImportError:
        print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} Installing requests library...{RESET}")
        return run_command(f"{sys.executable} -m pip install requests", 
                         "Installing requests via pip")


def install_stem():
    """
    Install the stem library for Tor control operations.
    """
    print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} Checking stem library...{RESET}")
    
    try:
        import stem
        print(f"{WHITE} [{GREEN}+{WHITE}]{GREEN} stem library is already installed.{RESET}")
        return True
    except ImportError:
        print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} Installing stem library...{RESET}")
        return run_command(f"{sys.executable} -m pip install stem", 
                         "Installing stem via pip")


def install_tor():
    """
    Install Tor service based on the operating system.
    """
    print(f"{WHITE} [{CYAN}~{WHITE}]{CYAN} Checking Tor installation...{RESET}")
    
    if is_command_available('tor'):
        print(f"{WHITE} [{GREEN}+{WHITE}]{GREEN} Tor is already installed.{RESET}")
        return True
    
    os_type = platform.system()
    
    if os_type == "Linux":
        if is_command_available('apt'):
            return run_command("sudo apt update && sudo apt install -y tor", 
                             "Installing Tor via apt")
        elif is_command_available('yum'):
            return run_command("sudo yum install -y tor", 
                             "Installing Tor via yum")
        elif is_command_available('dnf'):
            return run_command("sudo dnf install -y tor", 
                             "Installing Tor via dnf")
        elif is_command_available('pacman'):
            return run_command("sudo pacman -S --noconfirm tor", 
                             "Installing Tor via pacman")
    elif os_type == "Darwin":  # macOS
        if is_command_available('brew'):
            return run_command("brew install tor", "Installing Tor via Homebrew")
        else:
            print(f"{WHITE} [{YELLOW}!{WHITE}] {YELLOW}Please install Homebrew first: /bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\"{RESET}")
    elif os_type == "Windows":
        print(f"{WHITE} [{YELLOW}!{WHITE}] {YELLOW}On Windows, please download and install Tor Browser from https://www.torproject.org{RESET}")
        print(f"{WHITE} [{YELLOW}!{WHITE}] {YELLOW}Or install Tor as a service manually.{RESET}")
        return False
    
    print(f"{WHITE} [{RED}!{WHITE}] {RED}Could not install Tor automatically. Please install it manually.{RESET}")
    return False


def check_system_requirements():
    """
    Check if all system requirements are met.
    
    Returns:
        dict: Dictionary with requirement status
    """
    requirements = {
        'python': sys.version_info >= (3, 6),
        'pip': is_command_available('pip') or is_command_available('pip3'),
        'tor': is_command_available('tor'),
        'internet': False  # Will be checked by main program
    }
    
    try:
        import requests
        requirements['requests'] = True
    except ImportError:
        requirements['requests'] = False
        
    try:
        import stem
        requirements['stem'] = True
    except ImportError:
        requirements['stem'] = False
    
    return requirements


def print_system_info():
    """
    Print detailed system information for debugging.
    """
    os_info = get_os_info()
    requirements = check_system_requirements()
    
    print(f"{WHITE} [{CYAN}+{WHITE}]{CYAN} System Information:{RESET}")
    print(f"{WHITE}   OS: {os_info['system']} {os_info['release']}{RESET}")
    print(f"{WHITE}   Architecture: {os_info['machine']}{RESET}")
    print(f"{WHITE}   Python: {sys.version.split()[0]}{RESET}")
    
    print(f"{WHITE} [{CYAN}+{WHITE}]{CYAN} Requirements Status:{RESET}")
    for req, status in requirements.items():
        if req == 'internet':
            continue  # Skip internet check here
        status_str = f"{GREEN}✓{RESET}" if status else f"{RED}✗{RESET}"
        print(f"{WHITE}   {req}: {status_str}{RESET}")


if __name__ == "__main__":
    print("Tornet Utils - System requirement checker")
    print_system_info()