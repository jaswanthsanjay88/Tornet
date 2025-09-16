# Tornet-suntzu

🧅 **Tornet** - A Python-based tool for automating IP address changes using the Tor network. Provides cross-platform support for Linux, macOS, and Windows with both command-line interface and programmatic control.

## ✨ Features

- **Cross-platform support**: Works on Linux, macOS, and Windows
- **Automated IP rotation**: Change your IP address at specified intervals
- **Multiple control methods**: Uses Tor control port (stem) or service reload
- **Real-time IP monitoring**: Display current IP with geolocation info
- **Verbose logging**: Detailed logging for debugging and monitoring
- **Auto-installation**: Automatically installs required dependencies
- **Browser configuration**: Guidance for setting up browser proxy settings

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Internet connection
- Administrative privileges (for Tor service management)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Tornet-suntzu
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Auto-install system requirements:**
   ```bash
   python tornet.py --auto-fix
   ```

## 📖 Usage

### Basic Commands

**Display current IP address:**
```bash
python tornet.py --ip
```

**Change IP every 60 seconds, 10 times:**
```bash
python tornet.py --interval 60 --count 10
```

**Run indefinitely with verbose output:**
```bash
python tornet.py --interval 30 --count 0 --verbose
```

**Stop all Tor services:**
```bash
python tornet.py --stop
```

### Command Line Options

```
Options:
  --interval INT     Time in seconds between IP changes (default: 60)
  --count INT        Number of IP changes. Use 0 for infinite (default: 10)
  --ip              Display current IP address and exit
  --auto-fix        Install/upgrade required packages automatically
  --stop            Stop all Tor services and processes
  --verbose, -v     Enable verbose debug output
  --version         Show version information
  --help, -h        Show help message
```

### Examples

**Monitor IP changes every 2 minutes:**
```bash
python tornet.py --interval 120 --count 5 --verbose
```

**Quick IP check:**
```bash
python tornet.py --ip
```

**Setup and fix environment:**
```bash
python tornet.py --auto-fix
```

## 🏗️ Project Structure

```
Tornet-suntzu/
├── tornet.py           # Main script - entry point
├── banner.py           # ASCII art banner display
├── utils.py            # System utilities and installation helpers
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies  
├── tests/              # Unit tests
│   ├── __init__.py
│   └── test_utils.py
├── logs/               # Log files (created automatically)
└── README.md           # This file
```

## 🧪 Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run tests with coverage
python -m pytest tests/ --cov=.
```

### Code Formatting

```bash
# Format code
black *.py

# Check code style
flake8 *.py

# Type checking
mypy *.py
```

## 🔧 Configuration

### Browser Setup

After starting Tornet, configure your browser to use the Tor proxy:

**Manual Proxy Configuration:**
- SOCKS Host: `127.0.0.1`
- Port: `9050` 
- Protocol: SOCKS v5

**Recommended:** Use Tor Browser which comes pre-configured.

### Tor Control Port

For faster IP changes, Tornet uses Tor's control port (9051) when available. The `stem` library enables this functionality.

### Logging

Logs are automatically saved to `logs/tornet_YYYYMMDD.log` with different verbosity levels:
- INFO: Basic operations and status
- DEBUG: Detailed debugging information (--verbose flag)

## 🎯 System Requirements

- **Python**: 3.6+
- **Dependencies**: `requests`, `stem`
- **System**: Tor service/daemon
- **Platform**: Linux, macOS, Windows

**Auto-detection and installation:**
- ✅ Checks Python version compatibility
- ✅ Installs pip if missing  
- ✅ Installs required Python packages
- ✅ Installs Tor via system package manager
- ✅ Configures and starts Tor service

## 🐛 Troubleshooting

### Common Issues

**"Tor is not installed"**
```bash
python tornet.py --auto-fix
```

**IP not changing**
- Ensure Tor service is running
- Try using verbose mode: `--verbose`
- Check logs in `logs/` directory

**Permission errors**
- Use `sudo` on Linux/macOS for service management
- Run as Administrator on Windows

**Connection timeout**
- Check internet connection
- Ensure Tor has time to connect (wait ~60 seconds)

### Platform-Specific Notes

**Linux:** Requires `sudo` for systemctl commands  
**macOS:** Requires Homebrew for automatic Tor installation  
**Windows:** Recommend using Tor Browser for simplest setup

## 📋 TODO / Roadmap

- [x] Cross-platform OS detection and support
- [x] Tor control port integration (stem library) 
- [x] Comprehensive logging system
- [x] Auto-installation of dependencies
- [x] Unit tests and code documentation
- [ ] Configuration file support
- [ ] GUI interface
- [ ] Docker container support
- [ ] Integration with VPN services
- [ ] Custom exit node selection

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests: `python -m pytest`
5. Format code: `black *.py`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and privacy purposes only. Users are responsible for complying with local laws and regulations. The authors are not responsible for any misuse of this software.

---

**Author:** Fidal (Enhanced by suntzu)  
**Version:** 2.1.0  
**Status:** Active Development
# Tornet
