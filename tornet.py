#tornet.py
#!/usr/bin/env python3

# -*- coding: utf-8 -*-

#

# tornet - Automate IP address changes using Tor

# Author: Fidal (patched for Arch Linux by ChatGPT, further adapted for OS-agnosticism and new features)

import os

import time

import argparse

import requests

import subprocess

import signal

import platform

import sys

import logging

from datetime import datetime

# Import stem for Tor control port (install with: pip install stem)

try:

    from stem.control import Controller

    from stem import Signal

    STEM_AVAILABLE = True

except ImportError:

    STEM_AVAILABLE = False

    print("\n[!] 'stem' library not found. Falling back to service reload for IP changes.")

    print("    Install with: pip install stem\n")

# Import local modules

from utils import install_pip, install_requests, install_stem, install_tor

from banner import print_banner

TOOL_NAME = "tornet"

# ANSI color codes

green = "\033[92m"

red = "\033[91m"

white = "\033[97m"

reset = "\033[0m"

cyan = "\033[36m"

yellow = "\033[93m" # Added yellow for warnings/debug

# Global variable for verbose mode

VERBOSE_MODE = False

# Configure logging

def setup_logging(verbose=False):

    """Configure logging based on verbosity level."""

    level = logging.DEBUG if verbose else logging.INFO

    log_format = '%(asctime)s - %(levelname)s - %(message)s'

    

    # Create logs directory if it doesn't exist

    os.makedirs('logs', exist_ok=True)

    

    # Configure logging to both file and console

    logging.basicConfig(

        level=level,

        format=log_format,

        handlers=[

            logging.FileHandler(f'logs/tornet_{datetime.now().strftime("%Y%m%d")}.log'),

            logging.StreamHandler(sys.stdout) if verbose else logging.NullHandler()

        ]

    )

    

    return logging.getLogger(__name__)

def get_os_type():

    """
    Detects the operating system.
    
    Returns:
        str: The operating system type - "Linux", "macOS", "Windows", or "Unknown"
    """

    system = platform.system()

    if system == "Linux":

        return "Linux"

    elif system == "Darwin":

        return "macOS"

    elif system == "Windows":

        return "Windows"

    else:

        return "Unknown"

def verbose_print(message):

    """Prints a message only if verbose mode is enabled."""

    if VERBOSE_MODE:

        print(f"{white} [{yellow}DEBUG{white}] {yellow}{message}{reset}")

    

    # Also log to file regardless of verbose mode

    logging.getLogger(__name__).debug(message)

def is_tor_installed():

    """
    Checks if Tor is installed based on OS type.
    
    Returns:
        bool: True if Tor is found and available, False otherwise
        
    Notes:
        - On Linux/macOS: Checks if 'tor' command is in PATH
        - On Windows: Checks common Tor Browser and standalone installation paths
    """

    os_type = get_os_type()

    if os_type == "Linux" or os_type == "macOS":

        try:

            subprocess.check_output('which tor', shell=True)

            return True

        except subprocess.CalledProcessError:

            verbose_print("Tor executable not found in PATH.")

            return False

    elif os_type == "Windows":

        # Check for Tor executable in common paths or Tor Browser.

        # This is a simplification; a more robust check might be needed.

        tor_path_tb = os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Tor Browser", "Browser", "TorBrowser", "Tor", "tor.exe")

        tor_path_system = os.path.join(os.environ.get("PROGRAMFILES", "C:\\Program Files"), "Tor", "tor.exe") # Example for standalone

        if os.path.exists(tor_path_tb) or os.path.exists(tor_path_system):

            verbose_print("Tor executable found in common Windows paths.")

            return True

        else:

            verbose_print("Tor executable not found in common Windows paths.")

            return False

    verbose_print(f"Tor installation check failed for unknown OS type: {os_type}")

    return False

def start_tor_service():

    """Starts the Tor service based on the detected OS."""

    os_type = get_os_type()

    verbose_print(f"Attempting to start Tor service on {os_type}")

    if os_type == "Linux":

        print(f"{white} [{green}+{white}]{green} Starting Tor service (systemctl)...{reset}")

        os.system("sudo systemctl start tor")

    elif os_type == "macOS":

        print(f"{white} [{green}+{white}]{green} Starting Tor service (brew services)...{reset}")

        os.system("brew services start tor") # Assuming Tor installed via Homebrew

    elif os_type == "Windows":

        print(f"{white} [{green}+{white}]{cyan} On Windows, please ensure Tor is running, e.g., via Tor Browser, or by starting 'tor.exe' manually.{reset}")

    else:

        print(f"{white} [{red}!{white}] {red}Unsupported OS for automatic Tor service start.{reset}")

def reload_tor_service():

    """Reloads the Tor service based on the detected OS to get a new IP."""

    os_type = get_os_type()

    verbose_print(f"Attempting to reload Tor service on {os_type}")

    if os_type == "Linux":

        print(f"{white} [{green}+{white}]{green} Reloading Tor service (systemctl)...{reset}")

        os.system("sudo systemctl reload tor")

    elif os_type == "macOS":

        print(f"{white} [{green}+{white}]{green} Restarting Tor service (brew services) to reload circuit...{reset}")

        os.system("brew services restart tor") # Homebrew's restart acts like a reload for new circuits

    elif os_type == "Windows":

        print(f"{white} [{cyan}~{white}]{cyan} On Windows, for a new Tor circuit, you usually need to restart Tor Browser or its underlying Tor process manually.{reset}")

        print(f"{white} [{cyan}~{white}]{cyan} This script cannot automate Tor circuit changes on Windows without direct control port access and specific Tor setup.{reset}")

    else:

        print(f"{white} [{red}!{white}] {red}Unsupported OS for automatic Tor service reload.{reset}")

def change_ip_via_control_port():

    """Sends a NEWNYM signal to Tor via its control port."""

    verbose_print("Attempting IP change via Tor control port.")

    if not STEM_AVAILABLE:

        verbose_print("stem library not available, cannot use control port.")

        return False

    try:

        # Default control port is 9051, no password for default Tor installations

        # If torrc has a HashedControlPassword, you'd need controller.authenticate("password")

        with Controller.from_port(port=9051) as controller:

            controller.authenticate()

            controller.signal(Signal.NEWNYM)

            print(f"{white} [{green}+{white}]{green} Sent NEWNYM signal to Tor for a new circuit.{reset}")

            return True

    except Exception as e:

        verbose_print(f"Error sending NEWNYM signal: {e}")

        print(f'{white} [{red}!{white}] {red}Failed to send NEWNYM signal via Tor control port: {e}. Falling back to service reload.{reset}')

        return False

def stop_tor_service_gracefully():

    """Stops the Tor service gracefully based on OS type, trying control port first."""

    os_type = get_os_type()

    verbose_print(f"Attempting to stop Tor service gracefully on {os_type}")

    if STEM_AVAILABLE:

        try:

            with Controller.from_port(port=9051) as controller:

                controller.authenticate()

                # Sending a SHUTDOWN signal is possible but often not ideal for stopping the service.

                # A better approach is to use OS service commands.

                verbose_print("Tor control port found, but using OS-specific stop command for service shutdown.")

        except Exception as e:

            verbose_print(f"Could not connect to Tor control port for graceful shutdown check: {e}")

    if os_type == "Linux":

        print(f"{white} [{green}+{white}]{green} Stopping Tor service (systemctl)...{reset}")

        os.system("sudo systemctl stop tor")

    elif os_type == "macOS":

        print(f"{white} [{green}+{white}]{green} Stopping Tor service (brew services)...{reset}")

        os.system("brew services stop tor")

    elif os_type == "Windows":

        print(f"{white} [{cyan}~{white}]{cyan} On Windows, if Tor Browser is used, close the browser to stop Tor. Otherwise, manually stop the Tor process.{reset}")

    else:

        print(f"{white} [{red}!{white}] {red}Unsupported OS for automatic Tor service stop.{reset}")

def configure_browser_for_tor():

    """

    Provides guidance to the user on how to configure their default browser for Tor.

    """

    os_type = get_os_type()

    print(f"\n{white} [{green}+{white}]{green} To use Tor for anonymity, you need to configure your browser.{reset}")

    print(f"{white} [{green}+{white}]{green} Here's general guidance for common browsers:{reset}")

    if os_type == "Windows":

        print(f"{white}   - {cyan}Firefox/Chrome (Windows):{reset} Go to browser settings -> Network Proxy. Select 'Manual proxy configuration' and set 'SOCKS Host' to '127.0.0.1' and 'Port' to '9050'. Select SOCKS v5. Leave HTTP/HTTPS proxies empty.")

        print(f"{white}   - {cyan}Tor Browser (Recommended for Windows):{reset} Tor Browser is pre-configured to use Tor. Just use it!")

    elif os_type == "macOS":

        print(f"{white}   - {cyan}Firefox/Chrome (macOS):{reset} Similar to Windows. Go to browser settings -> Network Proxy. Select 'Manual proxy configuration' and set 'SOCKS Host' to '127.0.0.1' and 'Port' to '9050'. Select SOCKS v5. Leave HTTP/HTTPS proxies empty.")

        print(f"{white}   - {cyan}System-wide Proxy (macOS):{reset} Go to System Settings -> Network -> (Your active network interface) -> Details -> Proxies. Check 'SOCKS Proxy' and set '127.0.0.1' and '9050'.")

        print(f"{white}   - {cyan}Tor Browser (Recommended for macOS):{reset} Tor Browser is pre-configured to use Tor. Just use it!")

    elif os_type == "Linux":

        print(f"{white}   - {cyan}Firefox/Chrome (Linux):{reset} Go to browser settings -> Network Proxy. Select 'Manual proxy configuration' and set 'SOCKS Host' to '127.0.0.1' and 'Port' to '9050'. Select SOCKS v5. Leave HTTP/HTTPS proxies empty.")

        print(f"{white}   - {cyan}System-wide Proxy (Linux):{reset} This varies by desktop environment (e.g., GNOME, KDE). Look for 'Network Proxy' settings in your system settings.")

        print(f"{white}   - {cyan}Tor Browser (Recommended for Linux):{reset} Tor Browser is pre-configured to use Tor. Just use it!")

    else:

        print(f"{white}   - {cyan}General Guidance:{reset} In your browser's network settings, look for proxy configuration. Set a SOCKS5 proxy to `127.0.0.1` on port `9050`.")

    print(f"{white} [{green}+{white}]{green} Remember to revert your browser's proxy settings when you're done using TorNet!{reset}")

def initialize_environment():

    verbose_print("Initializing environment...")

    install_pip()

    install_requests()

    install_stem() # Install stem library

    install_tor()

    start_tor_service()

    print_start_message()

    configure_browser_for_tor() # Add browser configuration guidance

def print_start_message():

    print(f"{white} [{green}+{white}]{green} Tor service started. Please wait a minute for Tor to connect.{reset}")

    print(f"{white} [{green}+{white}]{green} Your current OS is: {platform.system()} {platform.release()} ({platform.machine()}){reset}")

def ma_ip():

    if is_tor_running():

        return ma_ip_tor()

    else:

        verbose_print("Tor not detected as running, fetching normal IP.")

        return ma_ip_normal()

def is_tor_running():

    """Checks if Tor process is running based on OS type."""

    os_type = get_os_type()

    verbose_print(f"Checking if Tor is running on {os_type}")

    if os_type == "Linux" or os_type == "macOS":

        try:

            subprocess.check_output('pgrep -x tor', shell=True)

            verbose_print("Tor process found via pgrep.")

            return True

        except subprocess.CalledProcessError:

            verbose_print("Tor process not found via pgrep.")

            return False

    elif os_type == "Windows":

        # On Windows, checking for a running Tor process is more complex.

        # Assuming if tor.exe is in a common path, it might be running.

        # A more robust check would involve listing processes and looking for 'tor.exe'.

        verbose_print("Cannot reliably check Tor running status on Windows without more specific process handling. Assuming running if Tor Browser is started.")

        return True # Assume it's running if the user was told to start it.

    verbose_print(f"Tor running status check failed for unknown OS type: {os_type}")

    return False

def get_ip_geolocation(ip_address):

    """Fetches approximate geolocation (country) for an IP address."""

    if not ip_address:

        return "Unknown"

    try:

        response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)

        response.raise_for_status()

        data = response.json()

        country = data.get('country_name', 'Unknown')

        return country

    except requests.RequestException as e:

        verbose_print(f"Could not fetch geolocation for {ip_address}: {e}")

        return "Unknown"

def ma_ip_tor():

    url = 'https://api.ipify.org'

    proxies = {

        'http': 'socks5h://127.0.0.1:9050',

        'https': 'socks5h://127.0.0.1:9050'

    }

    try:

        verbose_print("Fetching IP via Tor proxy.")

        response = requests.get(url, proxies=proxies, timeout=30)

        response.raise_for_status()

        return response.text.strip()

    except requests.exceptions.Timeout:

        print(f'{white} [{red}!{white}] {red}Tor connection timed out. Tor may not be fully connected yet.{reset}')

        verbose_print("Tor IP fetch timed out.")

        return None

    except requests.RequestException as e:

        print(f'{white} [{red}!{white}] {red}Having trouble connecting to the Tor network: {e}. Is Tor running and connected?{reset}')

        verbose_print(f"Error fetching IP via Tor: {e}")

        return None

def ma_ip_normal():

    try:

        verbose_print("Fetching normal IP.")

        response = requests.get('https://api.ipify.org', timeout=10)

        response.raise_for_status()

        return response.text.strip()

    except requests.exceptions.Timeout:

        print(f'{white} [{red}!{white}] {red}Normal IP fetch timed out. Check your internet connection.{reset}')

        verbose_print("Normal IP fetch timed out.")

        return None

    except requests.RequestException as e:

        print(f'{white} [{red}!{white}] {red}Having trouble fetching the IP address: {e}. Please check your internet connection.{reset}')

        verbose_print(f"Error fetching normal IP: {e}")

        return None

def change_ip(max_retries=3, ip_check_interval=5):

    """

    Changes the IP and verifies it, with retries.

    Tries NEWNYM signal first, then falls back to service reload.

    """

    verbose_print("Attempting to change IP.")

    current_ip_before_change = ma_ip_tor() # Get current IP to verify change

    if not current_ip_before_change:

        print(f'{white} [{red}!{white}] {red}Could not get current Tor IP. Cannot verify IP change.{reset}')

        # Proceed with change anyway, as Tor might just be slow to connect

        pass

    for attempt in range(1, max_retries + 1):

        print(f"{white} [{cyan}~{white}]{cyan} IP change attempt {attempt}/{max_retries}...{reset}")

        # Try control port first if available

        if STEM_AVAILABLE and change_ip_via_control_port():

            pass # Signal sent

        else:

            reload_tor_service() # Fallback to service reload

        # Give Tor a moment to establish a new circuit

        time.sleep(ip_check_interval)

        new_ip = ma_ip_tor()

        if new_ip and new_ip != current_ip_before_change:

            print(f'{white} [{green}+{white}]{green} Successfully changed IP.{reset}')

            return new_ip

        elif new_ip and new_ip == current_ip_before_change:

            print(f'{white} [{yellow}WARNING{white}] {yellow}IP address did not change on attempt {attempt}. Retrying...{reset}')

        else:

            print(f'{white} [{yellow}WARNING{white}] {yellow}Failed to obtain new IP on attempt {attempt}. Retrying...{reset}')

        

        # Update current_ip_before_change for the next attempt's comparison

        current_ip_before_change = new_ip if new_ip else current_ip_before_change

        

    print(f'{white} [{red}!{white}] {red}Failed to change IP after {max_retries} attempts.{reset}')

    return None # Return None if IP change ultimately failed

def change_ip_repeatedly(interval, count):

    if count == 0:

        while True:

            print(f"\n{white} [{cyan}~{white}]{cyan} Waiting {interval} seconds before changing IP...{reset}")

            time.sleep(interval)

            new_ip = change_ip()

            if new_ip:

                print_ip(new_ip)

    else:

        for i in range(count):

            print(f"\n{white} [{cyan}~{white}]{cyan} Waiting {interval} seconds before changing IP ({i+1}/{count})...{reset}")

            time.sleep(interval)

            new_ip = change_ip()

            if new_ip:

                print_ip(new_ip)

def print_ip(ip):

    country = get_ip_geolocation(ip)

    print(f'{white} [{green}+{white}]{green} Your IP has been changed to {white}:{green} {ip} {white}({country}){reset}')

def auto_fix():

    verbose_print("Running auto-fix...")

    install_pip()

    install_requests()

    install_stem() # Ensure stem is installed during auto-fix

    install_tor()

    # The 'pip install --upgrade tornet' line assumes 'tornet' is a PyPI package.

    # If it's a local script, this line should be removed or adapted.

    print(f"{white} [{cyan}~{white}]{cyan} Assuming 'tornet' is a pip-installable package. If not, this step might not apply.{reset}")

    try:

        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', TOOL_NAME])

    except subprocess.CalledProcessError:

        print(f"{white} [{yellow}WARNING{white}] {yellow}Could not upgrade {TOOL_NAME} via pip. If this is a local script, ignore this warning.{reset}")

def stop_services():

    verbose_print("Stopping services...")

    stop_tor_service_gracefully()

    os.system("pkill -f tornet > /dev/null 2>&1") # Kills any running tornet script

    print(f"{white} [{green}+{white}]{green} Tor services and {TOOL_NAME} processes stopped.{reset}")

def signal_handler(sig, frame):

    stop_services()

    print(f"\n{white} [{red}!{white}] {red}Program terminated by user.{reset}")

    exit(0)

def check_internet_connection():

    print(f"{white} [{cyan}~{white}]{cyan} Checking internet connection...{reset}")

    for _ in range(3): # Try a few times

        time.sleep(1)

        try:

            requests.get('http://www.google.com', timeout=3)

            print(f"{white} [{green}+{white}]{green} Internet connection OK.{reset}")

            return True

        except requests.RequestException:

            print(f"{white} [{red}!{white}] {red}Internet connection failed. Retrying...{reset}")

    print(f"{white} [{red}!{white}] {red}Could not establish internet connection. Exiting.{reset}")

    exit(1)

def main():

    global VERBOSE_MODE # Declare global to modify

    signal.signal(signal.SIGINT, signal_handler)

    signal.signal(signal.SIGQUIT, signal_handler)

    parser = argparse.ArgumentParser(description="TorNet - Automate IP address changes using Tor")

    parser.add_argument('--interval', type=int, default=60, help='Time in seconds between IP changes')

    parser.add_argument('--count', type=int, default=10, help='Number of times to change the IP. If 0, change IP indefinitely')

    parser.add_argument('--ip', action='store_true', help='Display the current IP address and exit')

    parser.add_argument('--auto-fix', action='store_true', help='Automatically fix issues (install/upgrade packages)')

    parser.add_argument('--stop', action='store_true', help='Stop all Tor services and tornet processes and exit')

    parser.add_argument('--version', action='version', version='%(prog)s 2.1.0') # Updated version

    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose/debug output')

    args = parser.parse_args()

    VERBOSE_MODE = args.verbose # Set global verbose mode

    

    # Setup logging

    logger = setup_logging(args.verbose)

    logger.info("Starting Tornet v2.1.0")

    if args.ip:

        ip = ma_ip()

        if ip:

            print_ip(ip)

        return

    if not is_tor_installed():

        print(f"{white} [{red}!{white}] {red}Tor is not installed or not found. Please install Tor (e.g., `sudo apt install tor` on Debian/Ubuntu, `brew install tor` on macOS, or Tor Browser on Windows) and try again.{reset}")

        return

    if args.auto_fix:

        auto_fix()

        print(f"{white} [{green}+{white}]{green} Auto-fix complete.{reset}")

        return

    if args.stop:

        stop_services()

        return

    check_internet_connection() # Check connection before starting TorNet operations

    print_banner()

    initialize_environment()

    change_ip_repeatedly(args.interval, args.count)

if __name__ == "__main__":

    main()