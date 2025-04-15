# ioc_enricher.py

import requests

# API Keys
VIRUSTOTAL_API_KEY = "0a3113ea071cab5b574e9901d7588bfdeda15449d69e856bbf964b4907d9c7de"
ABUSEIPDB_API_KEY = "77743d316f3373c5854b62ffe7ab712a2d25f231102c6c87326e86b6315da1d07eceaa6dfd95f03f"
SHODAN_API_KEY = "89nvDKjiiQaDuUtd6xzTbMK7i5An0P9Q"

# Other Service URLs
TALOS_LOOKUP_URL = "https://talosintelligence.com/reputation_center/lookup?search="
GREYNOISE_LOOKUP_URL = "https://viz.greynoise.io/ip/"

def check_virustotal(ip):
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_abuseipdb(ip):
    url = "https://api.abuseipdb.com/api/v2/check"
    params = {
        'ipAddress': ip,
        'maxAgeInDays': '90'
    }
    headers = {
        'Key': ABUSEIPDB_API_KEY,
        'Accept': 'application/json'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def check_shodan(ip):
    url = f"https://api.shodan.io/shodan/host/{ip}?key={SHODAN_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def enrich_ioc(ip):
    """
    Given an IP, enrich it with VirusTotal, AbuseIPDB, Shodan, and prepare links for Talos and GreyNoise
    """
    enriched_data = {}

    print(f"\n🔍 Enriching {ip}...")

    # VirusTotal
    vt_result = check_virustotal(ip)
    if vt_result:
        enriched_data["VirusTotal"] = vt_result
    else:
        enriched_data["VirusTotal"] = "Not Found"

    # AbuseIPDB
    abuse_result = check_abuseipdb(ip)
    if abuse_result:
        enriched_data["AbuseIPDB"] = abuse_result
    else:
        enriched_data["AbuseIPDB"] = "Not Found"

    # Shodan
    shodan_result = check_shodan(ip)
    if shodan_result:
        enriched_data["Shodan"] = shodan_result
    else:
        enriched_data["Shodan"] = "Not Found"

    # Talos Link
    enriched_data["Talos Lookup URL"] = TALOS_LOOKUP_URL + ip

    # GreyNoise Link
    enriched_data["GreyNoise Lookup URL"] = GREYNOISE_LOOKUP_URL + ip

    return enriched_data

if __name__ == "__main__":
    import json

    # Example usage
    with open("extracted_leaks.json", "r") as file:
        leaks = json.load(file)

    all_enriched = {}

    for ip in leaks.get("ip_addresses", []):
        enriched = enrich_ioc(ip)
        all_enriched[ip] = enriched

    with open("enriched_iocs.json", "w", encoding="utf-8") as out_file:
        json.dump(all_enriched, out_file, indent=4)

    print("\n✅ Enrichment complete! Data saved to enriched_iocs.json.")
