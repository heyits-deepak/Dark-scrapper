import os
import json
from data_collection.tor_scraper import scrape
from data_collection.bs4_parser import extract_leaks_from_html
from ioc_extraction.ioc_validator import check_virustotal
from mitre_mapping.mitre_mapper import classify_threats
from mitre_mapping.report_generator import generate_report

# Define target .onion URL
TARGET_URL = "TARGET_ONION_LINK"

def main():
    print("\n🚀 Starting Dark Web Threat Analysis...")

    # Step 1: Scrape the Dark Web Page
    print("\n🔍 Scraping website...")
    soup = scrape(TARGET_URL)
    if not soup:
        print("[ERROR] Scraping failed. Exiting.")
        return
    
    with open("scraped_page.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    print("[INFO] HTML content saved for analysis.")

    # Step 2: Extract Leaked Data
    print("\n📊 Extracting leaked data from HTML...")
    extracted_data = extract_leaks_from_html("scraped_page.html")

    with open("extracted_leaks.json", "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, indent=4)
    print("[INFO] Extracted leaks saved.")

    # Step 3: Validate IOCs against VirusTotal
    print("\n🔎 Validating IOCs with VirusTotal...")
    validated_leaks = {**extracted_data}  # Copy extracted data

    for ip in extracted_data["ip_addresses"]:
        result = check_virustotal(ip)
        validated_leaks[ip] = "Malicious" if result else "Clean"

    # Save validated IOCs
    with open("validated_leaks.json", "w", encoding="utf-8") as json_file:
        json.dump(validated_leaks, json_file, indent=4)
    print("[INFO] IOC validation completed.")

    # Step 4: Map Threats to MITRE ATT&CK
    print("\n⚠️ Mapping threats to MITRE ATT&CK...")
    mapped_threats = classify_threats(validated_leaks)

    with open("threat_mapping.json", "w", encoding="utf-8") as json_file:
        json.dump(mapped_threats, json_file, indent=4)
    print("[INFO] Threat mapping saved.")

    # Step 5: Generate Final Threat Report
    print("\n📜 Generating final threat report...")
    generate_report()

    print("\n✅ All tasks completed successfully! Check `final_report.json`.")

if __name__ == "__main__":
    main()
