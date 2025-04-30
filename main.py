import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data_collection.tor_scraper import scrape
from data_collection.bs4_parser import extract_leaks_from_html

from ioc_extraction.ioc_validator import (
    check_virustotal,
    check_abuseipdb,
    check_shodan,
    enrich_ioc,
)

from mitre_mapping.mitre_mapper import classify_threats
from mitre_mapping.report_generator import generate_report

app = FastAPI()

# Allow your frontend (e.g., React at localhost:3000) to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URL(BaseModel):
    url: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/get-url")
async def get_url(request: URL):
    url_value = request.url
    print("\n🚀 Starting Dark Web Threat Analysis for:", url_value)

    # Step 1: Scrape the target page
    print("🔍 Scraping website...")
    soup = scrape(url_value)
    if not soup:
        print("[ERROR] Scraping failed.")
        raise HTTPException(status_code=500, detail="Failed to scrape the provided URL")
    html_content = str(soup)
    with open("scraped_page.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("[INFO] Saved scraped_page.html")

    # Step 2: Extract leaked data (IOCs)
    print("📊 Extracting leaked data from HTML...")
    extracted_data = extract_leaks_from_html("scraped_page.html")
    with open("extracted_leaks.json", "w", encoding="utf-8") as f:
        json.dump(extracted_data, f, indent=4)
    print("[INFO] Saved extracted_leaks.json")

    # Step 3: Enrich each IP IOC with multiple services
    print("🔎 Enriching IOCs (VirusTotal, AbuseIPDB, Shodan, Talos, GreyNoise)...")
    enriched_iocs = {}
    for ip in extracted_data.get("leaks", {}).get("ip_addresses", []):
        enriched_iocs[ip] = enrich_ioc(ip)
    with open("enriched_iocs.json", "w", encoding="utf-8") as f:
        json.dump(enriched_iocs, f, indent=4)
    print("[INFO] Saved enriched_iocs.json")

    # Step 3b: Build validated_leaks dict that retains 'leaks' key for MITRE mapper
    validated_leaks = {**extracted_data}
    for ip, data in enriched_iocs.items():
        vt = data.get("VirusTotal", {})
        stats = vt.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        malicious_count = stats.get("malicious", 0)
        validated_leaks[ip] = "Malicious" if malicious_count > 0 else "Clean"
    with open("validated_leaks.json", "w", encoding="utf-8") as f:
        json.dump(validated_leaks, f, indent=4)
    print("[INFO] Saved validated_leaks.json")

    # Step 4: Map to MITRE ATT&CK
    print("⚠️ Mapping threats to MITRE ATT&CK...")
    mapped_threats = classify_threats(validated_leaks)
    with open("threat_mapping.json", "w", encoding="utf-8") as f:
        json.dump(mapped_threats, f, indent=4)
    print("[INFO] Saved threat_mapping.json")

    # Step 5: Generate final report
    print("📜 Generating final threat report...")
    report = generate_report()  # Assumes this writes final_report.json internally
    print("✅ All tasks completed! See final_report.json for details.")

    return report
