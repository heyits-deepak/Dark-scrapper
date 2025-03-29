import requests
from bs4 import BeautifulSoup
from stem import Signal
from stem.control import Controller
import os
from dotenv import load_dotenv

# Load environment variables from `.env`
load_dotenv()
TOR_PASSWORD = os.getenv("Your_pass")

# Function to rotate TOR IP
def renew_connection():
    """
    Sends a NEWNYM signal to TOR to change exit nodes.
    """
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate(password=TOR_PASSWORD)
            controller.signal(Signal.NEWNYM)
            print("[INFO] TOR IP address rotated successfully.")
    except Exception as e:
        print(f"[ERROR] Failed to rotate TOR IP: {e}")

# Function to scrape a dark web page using TOR
def scrape(url):
    """
    Scrapes a .onion website through TOR proxy.
    """
    session = requests.Session()
    session.proxies = {
        "http": "socks5h://127.0.0.1:9050",
        "https": "socks5h://127.0.0.1:9050"
    }

    try:
        response = session.get(url, timeout=30)  # Increased timeout
        if response.status_code == 200:
            print(f"[INFO] Successfully scraped: {url}")
            return BeautifulSoup(response.text, "html.parser")
        else:
            print(f"[ERROR] Failed to fetch {url}. Status: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] {e}")
        return None

# Main Execution
if __name__ == "__main__":
    onion_url = "http://tortaxiprd6ybez7n7fnwwmcdo3efib5hv6z7ks463ya72bv7ovz7qqd.onion/journal.html"  # Replace with actual .onion site

    # Rotate TOR IP before making a request
    renew_connection()

    # Scrape the onion site
    soup = scrape(onion_url)

    if soup:
        with open("scraped_page.html", "w", encoding="utf-8") as file:
            file.write(str(soup))
        print("[INFO] HTML content saved for parsing.")
    else:
        print("[ERROR] Failed to scrape the page.")
