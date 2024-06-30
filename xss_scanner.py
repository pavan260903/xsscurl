import requests
from bs4 import BeautifulSoup
import argparse
import concurrent.futures
from urllib.parse import urljoin
from colorama import init, Fore, Style
import time

init(autoreset=True)

# Define color variables
red = Fore.RED
white = Fore.WHITE
green = Fore.GREEN
cyan = Fore.CYAN
end = Style.RESET_ALL

def load_payloads(file_path='payloads.txt'):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"{Fore.RED}Error loading payloads: {e}")
        return []

def scan_form(url, form, payloads):
    action = form.get("action")
    method = form.get("method", "get").lower()
    inputs = form.find_all("input")
    form_url = urljoin(url, action)

    for payload in payloads:
        data = {input.get("name"): payload for input in inputs if input.get("name")}

        if method == "post":
            result = requests.post(form_url, data=data)
        else:
            result = requests.get(form_url, params=data)

        if payload in result.text:
            print(f"{Fore.RED}Potential XSS vulnerability found in form with payload: {payload}")
            return True

    return False

def scan_url(url, payloads):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        forms = soup.find_all("form")
        if forms:
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(scan_form, url, form, payloads) for form in forms]
                for future in concurrent.futures.as_completed(futures):
                    if future.result():
                        break
        else:
            print(f"{Fore.YELLOW}No forms found on {url}")

    except Exception as e:
        print(f"{Fore.RED}Error scanning URL: {e}")

def display_logo():
    logo = """
    

                                  _____                    _____                    _____                    _____                    _____                    _____  
        ______                   /\    \                  /\    \                  /\    \                  /\    \                  /\    \                  /\    \ 
       |::|   |                 /::\    \                /::\    \                /::\    \                /::\____\                /::\    \                /::\____\
       |::|   |                /::::\    \              /::::\    \              /::::\    \              /:::/    /               /::::\    \              /:::/    /
       |::|   |               /::::::\    \            /::::::\    \            /::::::\    \            /:::/    /               /::::::\    \            /:::/    / 
       |::|   |              /:::/\:::\    \          /:::/\:::\    \          /:::/\:::\    \          /:::/    /               /:::/\:::\    \          /:::/    /  
       |::|   |             /:::/__\:::\    \        /:::/__\:::\    \        /:::/  \:::\    \        /:::/    /               /:::/__\:::\    \        /:::/    /   
       |::|   |             \:::\   \:::\    \       \:::\   \:::\    \      /:::/    \:::\    \      /:::/    /               /::::\   \:::\    \      /:::/    /    
       |::|   |           ___\:::\   \:::\    \    ___\:::\   \:::\    \    /:::/    / \:::\    \    /:::/    /      _____    /::::::\   \:::\    \    /:::/    /     
 ______|::|___|___ ____  /\   \:::\   \:::\    \  /\   \:::\   \:::\    \  /:::/    /   \:::\    \  /:::/____/      /\    \  /:::/\:::\   \:::\____\  /:::/    /      
|:::::::::::::::::|    |/::\   \:::\   \:::\____\/::\   \:::\   \:::\____\/:::/____/     \:::\____\|:::|    /      /::\____\/:::/  \:::\   \:::|    |/:::/____/       
|:::::::::::::::::|____|\:::\   \:::\   \::/    /\:::\   \:::\   \::/    /\:::\    \      \::/    /|:::|____\     /:::/    /\::/   |::::\  /:::|____|\:::\    \       
 ~~~~~~|::|~~~|~~~       \:::\   \:::\   \/____/  \:::\   \:::\   \/____/  \:::\    \      \/____/  \:::\    \   /:::/    /  \/____|:::::\/:::/    /  \:::\    \      
       |::|   |           \:::\   \:::\    \       \:::\   \:::\    \       \:::\    \               \:::\    \ /:::/    /         |:::::::::/    /    \:::\    \     
       |::|   |            \:::\   \:::\____\       \:::\   \:::\____\       \:::\    \               \:::\    /:::/    /          |::|\::::/    /      \:::\    \    
       |::|   |             \:::\  /:::/    /        \:::\  /:::/    /        \:::\    \               \:::\__/:::/    /           |::| \::/____/        \:::\    \   
       |::|   |              \:::\/:::/    /          \:::\/:::/    /          \:::\    \               \::::::::/    /            |::|  ~|               \:::\    \  
       |::|   |               \::::::/    /            \::::::/    /            \:::\    \               \::::::/    /             |::|   |                \:::\    \ 
       |::|   |                \::::/    /              \::::/    /              \:::\____\               \::::/    /              \::|   |                 \:::\____\
       |::|___|                 \::/    /                \::/    /                \::/    /                \::/____/                \:|   |                  \::/    /
        ~~                       \/____/                  \/____/                  \/____/                  ~~                       \|___|                   \/____/ 
                                                                                                                                                                      


    """
    print(cyan + logo)
    print('%s\n\tXSSCURL %sv3.1.5\n%s' % (red, white, end))

def startup_sequence():
    steps = [
        "Initializing...",
        "Loading payloads...",
        "Establishing secure connection...",
        "Setting up environment...",
        "Launching XSSCURL..."
    ]
    
    for step in steps:
        print(green + "[*] " + step)
        time.sleep(1)
    print(green + "[*] All systems go!\n")

def print_help():
    help_text = f"""
{red}XSSCURL v3.1.5{end}
{cyan}A Simple XSS Scanner{end}

{green}Usage:{end}
    python xss_scanner.py <url>

{green}Options:{end}
    <url>                       The URL to scan for XSS vulnerabilities

{green}Example:{end}
    python xss_scanner.py http://example.com

{green}How It Works:{end}
    XSSCURL scans the specified URL for XSS vulnerabilities by injecting a set of predefined payloads into forms found on the page.
    If a payload is reflected in the page's response, the tool will report a potential XSS vulnerability.

{green}Payloads:{end}
    The payloads used for the scan are loaded from a file named {cyan}payloads.txt{end}.
    You can add more advanced payloads to this file to enhance the scanning capabilities.

{green}Contributing:{end}
    Contributions are welcome! If you have suggestions or improvements, please submit a pull request on GitHub.
    [https://github.com/YOUR_USERNAME/xss_scanner](https://github.com/YOUR_USERNAME/xss_scanner)
"""
    print(help_text)

def main():
    display_logo()
    startup_sequence()
    parser = argparse.ArgumentParser(description="A Simple XSS Scanner")

    parser.add_argument("url", help="URL to scan for XSS vulnerabilities")

    args = parser.parse_args()
    
    if args.url == "-h" or args.url == "--help":
        print_help()
        return

    payloads = load_payloads()
    print(f"{Fore.GREEN}Scanning {args.url} for XSS vulnerabilities...")
    scan_url(args.url, payloads)
    print(f"{Fore.GREEN}Scan complete.")

if __name__ == "__main__":
    main()
