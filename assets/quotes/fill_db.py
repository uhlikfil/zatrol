import json

import requests

if __name__ == "__main__":
    with open("quotes.json", "r") as f:
        bodies = json.load(f)
    for body in bodies:
        requests.post("http://localhost:8000/api/quote", json=body)
