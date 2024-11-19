import socket
import sys
from concurrent.futures import ThreadPoolExecutor

def scan_port(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout para la conexión (puedes ajustarlo)
            result = s.connect_ex((ip, port))
            if result == 0:
                print(f"El puerto {port} está abierto")
    except Exception as e:
        print(f"No se pudo escanear el puerto {port}. Error: {e}")

def main(ip, start_port, end_port):
    with ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, ip, port)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: script.py <IP> <Puerto inicial> <Puerto final>")
        sys.exit(1)

    ip = sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    main(ip, start_port, end_port)
