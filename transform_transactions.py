# transform_transactions.py
import json
import re
from datetime import datetime


def extract_amount(body):
    """Extract amount in RWF from SMS body"""
    # Pattern for amounts like "1,000 RWF" or "2000 RWF"
    match = re.search(r'(\d{1,3}(?:,\d{3})*)\s*RWF', body)
    if match:
        return int(match.group(1).replace(',', ''))
    
    # Fallback pattern for amounts without commas
    match = re.search(r'(\d+)\s*RWF', body)
    return int(match.group(1)) if match else None


def extract_parties(body, transaction_type):
    """Extract sender and receiver based on transaction type"""
    sender = None
    receiver = None
    
    body_lower = body.lower()
    
    if transaction_type == "money_received":
        # "You have received X from Jane Smith"
        match = re.search(r'from\s+([A-Za-z\s]+?)(?:\s+\(|\son|\.)', body, re.IGNORECASE)
        if match:
            sender = match.group(1).strip()
        receiver = "You"
    
    elif transaction_type in ["money_transfer", "payment_to_person"]:
        # "X transferred to Samuel Carter" or "Your payment to Jane Smith"
        match = re.search(r'(?:to|transferred to)\s+([A-Za-z\s]+?)(?:\s+\(|\s+\d|\.|$)', body, re.IGNORECASE)
        if match:
            receiver = match.group(1).strip()
        sender = "You"
    
    elif transaction_type == "cash_withdrawal":
        # "withdrawn via agent: Agent Sophia"
        match = re.search(r'agent:\s*([A-Za-z\s]+?)(?:,|\))', body, re.IGNORECASE)
        if match:
            receiver = match.group(1).strip() + " (Agent)"
        sender = "You"
    
    elif transaction_type == "bank_deposit":
        sender = "Bank"
        receiver = "You"
    
    elif transaction_type == "airtime_purchase":
        sender = "You"
        receiver = "MTN Airtime"
    
    elif transaction_type == "cash_power":
        sender = "You"
        receiver = "Utility Company"
    
    elif transaction_type == "data_bundle":
        sender = "You"
        receiver = "MTN Data Services"
    
    elif transaction_type == "merchant_payment":
        # "by DIRECT PAYMENT LTD" or "by ESICIA LTD KPAY"
        match = re.search(r'by\s+([A-Za-z\s]+?(?:LTD|INC|Co\.)?)(?:\s+on|$)', body, re.IGNORECASE)
        if match:
            receiver = match.group(1).strip()
        sender = "You"
    
    elif transaction_type == "service_deduction":
        sender = "You"
        receiver = "Service Provider"
    
    else:
        sender = "Unknown"
        receiver = "Unknown"
    
    return sender, receiver


def detect_transaction_type(body):
    """Detect the type of financial transaction from SMS body"""
    body_lower = body.lower()
    
    # Check in order of specificity
    if "you have received" in body_lower:
        return "money_received"
    
    elif "*113*r*a bank deposit" in body_lower:
        return "bank_deposit"
    
    elif "withdrawn" in body_lower and "via agent" in body_lower:
        return "cash_withdrawal"
    
    elif "*165*s*" in body_lower and "transferred" in body_lower:
        return "money_transfer"
    
    elif "txid:" in body_lower and "your payment of" in body_lower:
        if "to airtime" in body_lower:
            return "airtime_purchase"
        elif "to mtn cash power" in body_lower:
            return "cash_power"
        elif "to bundles and packs" in body_lower:
            return "data_bundle"
        elif "to " in body_lower:
            return "payment_to_person"
    
    elif "*164*s*y'ello,a transaction of" in body_lower:
        return "merchant_payment"
    
    elif "direct payment ltd" in body_lower:
        return "service_deduction"
    
    elif "by " in body_lower and " on your momo account" in body_lower:
        return "merchant_payment"
    
    return "other"


def parse_timestamp(readable_date):
    """Convert readable date to ISO format"""
    if not readable_date:
        return None
    
    try:
        # "10 May 2024 4:30:58 PM" 
        dt = datetime.strptime(readable_date, "%d %b %Y %I:%M:%S %p")
        return dt.isoformat()
    except ValueError:
        # Try alternative format if needed
        try:
            dt = datetime.strptime(readable_date, "%d %b %Y %H:%M:%S")
            return dt.isoformat()
        except:
            return readable_date


def transform_sms_to_api_format(raw_sms):
    """Transform SMS data to API-required format"""
    api_ready_transactions = []
    
    for index, sms in enumerate(raw_sms, start=1):
        body = sms.get("body", "")
        
        # Skip non-financial messages
        body_lower = body.lower()
        if "one-time password" in body_lower or "dear customer" in body_lower:
            continue
        if "kanda" in body_lower and "poromosiyo" in body_lower:  # Promotional
            continue
        if "yello!" in body_lower and "umaze kugura" in body_lower:  # Data bundle confirmation
            # This is handled by the main detection, but skip if standalone
            continue
        
        transaction_type = detect_transaction_type(body)
        amount = extract_amount(body)
        
        # Skip if no amount (non-financial) or if it's "other" type
        if not amount or transaction_type == "other":
            continue
        
        sender, receiver = extract_parties(body, transaction_type)
        
        transaction = {
            "id": str(index),
            "transaction_type": transaction_type,
            "amount": amount,
            "currency": "RWF",
            "sender": sender,
            "receiver": receiver,
            "timestamp": parse_timestamp(sms.get("readable_date", "")),
            "description": body[:150] + "..." if len(body) > 150 else body,
            "original_sms_date": sms.get("readable_date")
        }
        
        api_ready_transactions.append(transaction)
    
    return api_ready_transactions


def analyze_transactions(transactions):
    """Print analysis of the transformed transactions"""
    print("\n📊 Transaction Analysis:")
    print("=" * 50)
    
    total_count = len(transactions)
    print(f"Total transactions: {total_count}")
    
    # Count by type
    type_counts = {}
    for t in transactions:
        t_type = t["transaction_type"]
        type_counts[t_type] = type_counts.get(t_type, 0) + 1
    
    print("\nTransaction Types:")
    for t_type, count in sorted(type_counts.items()):
        percentage = (count / total_count) * 100
        print(f"  {t_type}: {count} ({percentage:.1f}%)")
    
    # Total amount
    total_amount = sum(t["amount"] for t in transactions if t["amount"])
    print(f"\nTotal amount (RWF): {total_amount:,}")
    
    # Sample transactions
    print("\nSample transactions:")
    for i in range(min(3, len(transactions))):
        print(f"\n{i+1}. {transactions[i]['transaction_type']}:")
        print(f"   Amount: {transactions[i]['amount']} RWF")
        print(f"   From: {transactions[i]['sender']}")
        print(f"   To: {transactions[i]['receiver']}")


if __name__ == "__main__":
    print(" Transforming SMS data to API format...")
    
    try:
        # Read raw SMS data created by parse_sms.py
        with open("api_ready_transactions.json", "r", encoding="utf-8") as f:
            raw_sms = json.load(f)
        
        print(f" Loaded {len(raw_sms)} raw SMS messages")
        
        # Transform to API format
        api_data = transform_sms_to_api_format(raw_sms)
        
        # Save API-ready data
        with open("api_ready_transactions.json", "w", encoding="utf-8") as f:
            json.dump(api_data, f, indent=2, ensure_ascii=False)
        
        print(f" Created api_ready_transactions.json with {len(api_data)} transactions")
        
        # Show analysis
        analyze_transactions(api_data)
        
        # Show first transaction as example
        if api_data:
            print("\n" + "=" * 50)
            print(" First transaction (full format):")
            print(json.dumps(api_data[0], indent=2))
        
    except FileNotFoundError:
        print(" Error: api_ready_transactions.json not found!")
        print("   Please run parse_sms.py first to create the file.")
    except json.JSONDecodeError:
        print(" Error: api_ready_transactions.json contains invalid JSON!")
    except Exception as e:
        print(f" Unexpected error: {str(e)}")