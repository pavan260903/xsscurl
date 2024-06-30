# XSSCURL v3.1.5

**XSSCURL** is a simple and effective XSS (Cross-Site Scripting) vulnerability scanner designed for web security enthusiasts and professionals. It helps identify potential XSS vulnerabilities by injecting a set of predefined payloads into forms found on a given URL.
 <!-- Replace with the actual logo path -->

## Features

- **Automatic Form Detection**: Scans for forms on the target web page.
- **XSS Payload Injection**: Uses a variety of payloads to test for XSS vulnerabilities.
- **Multi-Threaded Scanning**: Speeds up the scanning process using concurrent requests.
- **Detailed Results**: Reports potential XSS vulnerabilities with the payload used.
- **Easy to Use**: Simple command-line interface with minimal setup.

## Installation

### Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `colorama` library

You can install the required libraries using `pip`:

```bash
pip install requests beautifulsoup4 colorama
