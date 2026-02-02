# parse_sms.py
import xml.etree.ElementTree as ET
import json


def parse_sms_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    transactions = []
    
    for i, sms in enumerate(root.findall("sms")):
        transaction = {
            "id": i,
            "protocol": sms.attrib.get("protocol"),
            "address": sms.attrib.get("address"),
            "date": sms.attrib.get("date"),
            "date_sent": sms.attrib.get("date_sent"),
            "readable_date": sms.attrib.get("readable_date"),
            "type": sms.attrib.get("type"),  # SMS direction (1=received, 2=sent)
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
    
    with open("api_ready_transactions.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f" XML successfully converted to JSON")
    print(f" Total SMS messages parsed: {len(data)}")