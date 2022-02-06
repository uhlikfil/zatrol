import json
import sys

import requests

if __name__ == "__main__":
    arg = sys.argv[1]
    with open(f"{arg}.json", "r") as f:
        bodies = json.load(f)
    for body in bodies:
        resp = requests.post(f"http://localhost:8000/api/{arg}", json=body)
        print(resp.status_code)
