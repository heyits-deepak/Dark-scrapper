import requests
import json

VIRUSTOTAL_API_KEY = "0a3113ea071cab5b574e9901d7588bfdeda15449d69e856bbf964b4907d9c7de"

def check_virustotal(ioc):
    """
    Checks an Indicator of Compromise (IOC) using VirusTotal API.
    """
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ioc}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    with open("extracted_leaks.json", "r") as file:
        leaks = json.load(file)

    for ip in leaks["ip_addresses"]:
        print(f"\n🔍 Checking {ip} in VirusTotal...")
        result = check_virustotal(ip)
        if result:
            print(f"⚠️ Threat detected: {result}")
        else:
            print(f"✅ No known threats for {ip}.")
