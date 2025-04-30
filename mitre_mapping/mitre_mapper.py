import json

# MITRE ATT&CK technique IDs for reference
MITRE_ATTACK_MAPPING = {
    "credential_leak": "T1555",   # Credentials from Password Stores
    "ip_suspicious": "T1071",     # Application Layer Protocol
    "domain_malware": "T1566"     # Phishing
}

def classify_threats(validated_data):
    """
    Maps extracted IOCs to relevant MITRE ATT&CK technique IDs.
    Returns a dictionary with string keys (no tuples).
    """
    mapping = {}

    # Map credentials
    for cred in validated_data["leaks"].get("credentials", []):
        username, password = cred
        key = f"cred::{username}:{password}"
        mapping[key] = MITRE_ATTACK_MAPPING["credential_leak"]

    # Map IPs
    for ip in validated_data["leaks"].get("ip_addresses", []):
        result = validated_data.get(ip, "Clean")
        if result == "Malicious":
            mapping[f"ip::{ip}"] = MITRE_ATTACK_MAPPING["ip_suspicious"]

    # Map domains
    for domain in validated_data["leaks"].get("domains", []):
        mapping[f"domain::{domain}"] = MITRE_ATTACK_MAPPING["domain_malware"]

    return mapping
