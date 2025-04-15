from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from data_collection.tor_scraper import scrape
from data_collection.bs4_parser import extract_leaks_from_html
from ioc_extraction.ioc_validator import check_virustotal
from ioc_extraction.ioc_enricher import enrich_ioc
from mitre_mapping.mitre_mapper import classify_threats
from mitre_mapping.report_generator import generate_report

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OnionURL(BaseModel):
    link: str

@app.post("/search")
async def analyze_onion(onion: OnionURL):
    try:
        target_url = onion.link.strip()

        # Step 1: Scrape Onion Page
        soup = scrape(target_url)
        if not soup:
            raise HTTPException(status_code=500, detail="Scraping failed or returned no data.")

        # Step 2: Extract Data
        extracted_data = extract_leaks_from_html(soup)
        if not extracted_data:
            raise HTTPException(status_code=500, detail="Leak extraction failed.")

        # Step 3: Validate IOCs
        ioc_status = {}
        for ip in extracted_data.get("ip_addresses", []):
            try:
                ioc_status[ip] = "Malicious" if check_virustotal(ip) else "Clean"
            except Exception:
                ioc_status[ip] = "Error during validation"

        # Step 4: Enrich IOCs
        enriched_data = {}
        for ip in extracted_data.get("ip_addresses", []):
            try:
                enriched_data[ip] = enrich_ioc(ip)
            except Exception:
                enriched_data[ip] = {"error": "Enrichment failed"}

        # Step 5: Map Threats to MITRE ATT&CK
        mitre_mapping = classify_threats(ioc_status)

        # Step 6: Generate Report (optional)
        try:
            generate_report()
        except Exception:
            pass  # You might want to log this error in a real system

        # Step 7: Return structured summary
        return {
            "message": "Analysis complete",
            "summary": {
                "leaks_found": extracted_data,
                "ioc_status": ioc_status,
                "ioc_enrichment": enriched_data,
                "threat_mapping": mitre_mapping
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
