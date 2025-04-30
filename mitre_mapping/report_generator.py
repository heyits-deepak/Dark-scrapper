import json

def generate_report():
    """
    Generates a final threat report combining extracted leaks and MITRE ATT&CK mapping.
    """
    with open("extracted_leaks.json", "r") as leaks_file:
        extracted_data = json.load(leaks_file)

    with open("threat_mapping.json", "r") as threats_file:
        threat_mapping = json.load(threats_file)

    leaks = extracted_data.get("leaks", {})

    report = {
        "summary": {
            "total_emails": len(leaks.get("emails", [])),
            "total_credentials": len(leaks.get("credentials", [])),
            "total_ips": len(leaks.get("ip_addresses", [])),
            "total_domains": len(leaks.get("domains", [])),
            "total_credit_cards": len(leaks.get("credit_cards", [])),
        },
        "threats": threat_mapping,
        "leaks": leaks
    }

    with open("final_report.json", "w", encoding="utf-8") as report_file:
        json.dump(report, report_file, indent=4)

    print("\n✅ Final report generated and saved as `final_report.json`\n")
    print("[📄 Final Report Preview]:\n")
    print(json.dumps(report, indent=4))

    return report

if __name__ == "__main__":
    generate_report()
