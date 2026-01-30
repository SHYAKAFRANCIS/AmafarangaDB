import json

def load_transactions(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Add ID to each transaction
    for i, tx in enumerate(data, start=1):
        tx["id"] = str(i)

    return data


if __name__ == "__main__":
    transactions = load_transactions("transactions.json")
    print(transactions[0])
    print(f"Total transactions: {len(transactions)}")
    print("✅ transactions loaded successfully")