#!/usr/bin/env python3
"""
Banner display module for Tornet
Provides ASCII art banner and visual formatting
"""

# ANSI color codes
green = "\033[92m"
red = "\033[91m"
white = "\033[97m"
reset = "\033[0m"
cyan = "\033[36m"


def print_banner():
    """
    Display the Tornet ASCII art banner with colors.
    
    This function prints a stylized banner showing the TORNET logo
    with the author attribution (suntzu).
    """
    banner = f"""
{white} +-------------------------------------------------------+
{white} |{green} ████████╗ ██████╗ ██████╗ ███╗   ██╗███████╗████████╗{white} |
{white} |{green} ╚══██╔══╝██╔═══██╗██╔══██╗████╗  ██║██╔════╝╚══██╔══╝{white} |
{white} |{green}    ██║   ██║   ██║██████╔╝██╔██╗ ██║█████╗     ██║   {white} |
{white} |{green}    ██║   ██║   ██║██╔══██╗██║╚██╗██║██╔══╝     ██║   {white} |
{white} |{green}    ██║   ╚██████╔╝██║  ██║██║ ╚████║███████╗   ██║   {white} |
{white} |{green}    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   {white} |
{white} +---------------------{cyan}({red}suntzu{cyan}){white}----------------------+{reset}
"""
    print(banner)