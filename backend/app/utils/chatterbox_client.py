import requests

class ChatterboxClient:
    def __init__(self, base_url="http://127.0.0.1:4123"):
        self.base_url = base_url

    def process_query(self, message, context):
        payload = {
            "input": message,
            "context": context
        }

        r = requests.post(
            f"{self.base_url}/chat",
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        return r.json()

    def generate_response(self, result, message):
        payload = {
            "input": message,
            "data": result
        }

        r = requests.post(
            f"{self.base_url}/respond",
            json=payload,
            timeout=10
        )
        r.raise_for_status()
        return r.json().get("response", "")

