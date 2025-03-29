import socks
import socket
from stem import Signal
from stem.control import Controller
from config.settings import TOR_PASSWORD

def set_tor_proxy():
    """
    Configures the system to route all requests through TOR.
    """
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
    socket.socket = socks.socksocket

def renew_tor_ip():
    """
    Requests a new TOR identity (IP address).
    """
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
            print("[INFO] TOR IP address rotated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to rotate TOR IP: {e}")

# Test function (Only for debugging, remove in production)
if __name__ == "__main__":
    print("[INFO] Setting up TOR proxy...")
    set_tor_proxy()
    print("[INFO] Rotating TOR IP...")
    renew_tor_ip()
