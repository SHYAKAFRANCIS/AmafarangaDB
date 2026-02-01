import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from auth import check_auth


def load_transactions():
    """Load the transactionns from the json file."""
    with open("api_transactions.json", "r", encoding="utf-8") as file:
        TRANSACTIONS = json.load(file)
    return TRANSACTIONS

    
class resourceHandler(BaseHTTPRequestHandler):
    """ handles the http requests for our transaction resource. """

    def send_json(self, status_code, data=None):
        self.send_response(status_code)
        self.send_header("content_type", "application/json")
        self.end_headers()

        if data is not None:
            self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        """ handles Get requests"""

        if not check_auth(self.headers):
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Transaction Realm"')
            self.end_headers()
            self.wfile.write(b" Unauthorized")
            return
    
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path != "/transactions":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found")
            return
        
        results = load_transactions()

        for key in ["type", "amount", "sender", "receiver", "timestamp"]:
            if key in query_params:
                value = query_params[key][0]
                results = [
                    tx for tx in results
                    if str(tx.get(key)) == value
                ]

        self.send_json(200, results)
    
    def do_POST(self):
        """ handles POST requests"""
        if not check_auth(self.headers):
            self.send_response(401)
            self.end_headers()
            return
        
        if self.path != "/transactions":
            self.send_respone(404)
            self.end_headers()
            return
        
        content_length = int(self.headers.get("content-length", 0))
        body = self.rfile.read(content_length)

        try: 
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        required_fields = ["type", "amount", "sender", "receiver", "timestamp"]
        for field in required_fields:
            if field not in data:
                self.send_response(400)
                self.end_headers()
                return
            
        transactions = load_transactions()
        transactions.append(data)

        with open("api_transactions.json", "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)
        
        self.send_json(201, data)



    def do_PUT(self):
        """ handles PUT requests"""
        if not check_auth(self.headers):
            self.send_response(401)
            self.end_headers()
            return
    
        parts = self.path.split("/")
        if len(parts) != 3 or parts[1] != "transactions":
            self.send_response(400)
            self.end_headers()
            return
    
        try:
            tx_id = int(parts[2])
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
    
        content_length = int(self.headers.get("Content_length", 0))
        body = self.rfile.read(content_length)

        try:
            updates = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return
    
        try:
            transactions = load_transactions()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            return
        
        # validation of transaction id
        if tx_id >= len(transactions) or tx_id < 0:
            self.send_response(404)
            self.end_headers()
            return
        
        try:
            transactions[tx_id].update(updates)
        except IndexError:
            self.send_response(404)
            self.end_headers()
            return
        
        #save it back to file
    
        with open("api_transactions.json", "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

        self.send_json(200, transactions[tx_id])

    def do_DELETE(self):
        """ handles DELETE requests"""
        if not check_auth(self.headers):
            self.send_response(401)
            self.end_headers()
            return
        
        parts = self.path.split("/")
        if len(parts) != 3 or parts[1] != "transactions":
            self.send_response(400)
            self.end_headers()
            return
        
        try:
            tx_id = int(parts[2])
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
        
        try:
            transactions = load_transactions()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            return
        # validation of transaction id
        if tx_id >= len(transactions) or tx_id < 0:
            self.send_response(404)
            self.end_headers()
            return
        deleted_tx = transactions.pop(tx_id)

        with open("api_transactions.json", "w", encoding="utf-8") as file:
            json.dump(transactions, file, indent=4)

        self.send_json(200, deleted_tx)
        

        
def run():
    """ run the server """ 
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, resourceHandler)
    print("Starting server on port 8000...")
    httpd.serve_forever()

if __name__ == "__main__":
    run() 




