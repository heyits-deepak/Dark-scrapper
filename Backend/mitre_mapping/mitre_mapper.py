import json

MITRE_ATTACK_MAPPING = {
    "credential_leak": "T1555",
    "ip_suspicious": "T1071",
    "domain_malware": "T1566"
}

def classify_threats(leaks):
    """
    Maps extracted IOCs to MITRE ATT&CK tactics.
    """
    threat_mapping = {}

    for ip in leaks["ip_addresses"]:
        threat_mapping[ip] = MITRE_ATTACK_MAPPING.get("ip_suspicious", "Unknown")

    for domain in leaks["domains"]:
        threat_mapping[domain] = MITRE_ATTACK_MAPPING.get("domain_malware", "Unknown")

    for credential in leaks["credentials"]:
        threat_mapping[credential] = MITRE_ATTACK_MAPPING.get("credential_leak", "Unknown")

    return threat_mapping

if __name__ == "__main__":
    with open("extracted_leaks.json", "r") as file:
        leaks = json.load(file)

    mapped_threats = classify_threats(leaks)

    with open("threat_mapping.json", "w") as file:
        json.dump(mapped_threats, file, indent=4)

    print("\n✅ Threats mapped to MITRE ATT&CK and saved in `threat_mapping.json`")
