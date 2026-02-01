import xml.etree.ElementTree as ET
import json

def parse_sms_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    transactions = []

    for sms in root.findall("sms"):
        transaction = {
            "protocol": sms.attrib.get("protocol"),
            "address": sms.attrib.get("address"),
            "date": sms.attrib.get("date"),
            "date_sent": sms.attrib.get("date_sent"),
            "readable_date": sms.attrib.get("readable_date"),
            "type": sms.attrib.get("type"),
            "body": sms.attrib.get("body"),
            "service_center": sms.attrib.get("service_center"),
            "contact_name": sms.attrib.get("contact_name"),
            "read": sms.attrib.get("read"),
            "status": sms.attrib.get("status")
        }

        transactions.append(transaction)

    return transactions


if __name__ == "__main__":
    xml_path = "modified_sms_v2.xml"
    data = parse_sms_xml(xml_path)

    # Print JSON
    print(json.dumps(data, indent=2))

    # Save JSON file
    with open("api_transactions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("✅ XML successfully converted to JSON")