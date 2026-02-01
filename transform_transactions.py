import json
import re


def extract_amount(body):
    match = re.search(r'(\d+)\s*RWF', body)
    return int(match.group(1)) if match else None


def extract_sender(body):
    match = re.search(r'from\s+([A-Za-z\s]+)', body)
    return match.group(1).strip() if match else None


def detect_transaction_type(body):
    body = body.lower()
    if "received" in body:
        return "Incoming Money"
    elif "sent" in body:
        return "Outgoing Money"
    elif "paid" in body or "payment" in body:
        return "Payment"
    elif "withdrawn" in body:
        return "Withdrawal"
    else:
        return "Unknown"


def transform_sms_to_transactions(raw_sms):
    transactions = []

    for index, sms in enumerate(raw_sms, start=1):
        body = sms.get("body", "")

        transaction = {
            "id": str(index),
            "transaction_type": detect_transaction_type(body),
            "amount": extract_amount(body),
            "sender": extract_sender(body),
            "receiver": "User",
            "timestamp": sms.get("readable_date")
        }

        transactions.append(transaction)

    return transactions


if __name__ == "__main__":
    with open("transactions.json", "r", encoding="utf-8") as f:
        raw_sms = json.load(f)

    api_transactions = transform_sms_to_transactions(raw_sms)

    with open("api_transactions.json", "w", encoding="utf-8") as f:
        json.dump(api_transactions, f, indent=2)

    print("✅ api_transactions.json created successfully")
