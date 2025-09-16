#!/usr/bin/env python3
"""
Unit tests for Tornet utility functions
"""

import pytest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import utils
from tornet import get_os_type, is_tor_installed


class TestUtils:
    """Test cases for utils.py functions"""

    def test_is_command_available(self):
        """Test command availability checking"""
        # Test with a command that should exist on most systems
        assert utils.is_command_available('python') or utils.is_command_available('python3')
        
        # Test with a command that should not exist
        assert not utils.is_command_available('nonexistent_command_12345')

    def test_get_os_info(self):
        """Test OS information gathering"""
        os_info = utils.get_os_info()
        
        assert isinstance(os_info, dict)
        assert 'system' in os_info
        assert 'release' in os_info
        assert 'machine' in os_info
        assert os_info['system'] in ['Linux', 'Darwin', 'Windows']

    def test_check_system_requirements(self):
        """Test system requirements checking"""
        requirements = utils.check_system_requirements()
        
        assert isinstance(requirements, dict)
        assert 'python' in requirements
        assert 'pip' in requirements
        assert requirements['python'] == True  # Should be True since we're running Python


class TestTornet:
    """Test cases for main tornet.py functions"""

    def test_get_os_type(self):
        """Test OS type detection"""
        os_type = get_os_type()
        assert os_type in ['Linux', 'macOS', 'Windows', 'Unknown']

    def test_is_tor_installed(self):
        """Test Tor installation detection"""
        # This test will pass regardless of whether Tor is installed
        # since it's testing the function logic, not Tor availability
        result = is_tor_installed()
        assert isinstance(result, bool)


if __name__ == "__main__":
    pytest.main([__file__])