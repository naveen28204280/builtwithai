import requests

class ChatterboxClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.chatterbox.ai/v1"  # Adjust based on actual API
    
    def process_query(self, user_message, context):
        """
        Send query to Chatterbox with financial context
        Returns structured intent and parameters
        """
        prompt = f"""
        Financial Context:
        - Current Balance: ${context.get('balance', 0)}
        - Monthly Spending: ${context.get('monthly_spending', 0)}
        - Recent Anomalies: {context.get('anomaly_count', 0)}
        - Available Categories: {', '.join(context.get('categories', []))}
        
        User Query: {user_message}
        
        Classify the intent and extract parameters:
        Possible intents: forecast, anomaly_check, spending_summary, budget_advice, whatif
        
        Return JSON format:
        {{
            "intent": "<intent_type>",
            "category": "<category_name or null>",
            "time_range": "<days or null>",
            "amount": <number or null>,
            "scenario": "<description or null>"
        }}
        """
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={
                "message": prompt,
                "model": "chatterbox-default"
            }
        )
        
        return response.json()
    
    def generate_response(self, data, query):
        """
        Convert structured data into natural language response
        """
        prompt = f"""
        User asked: {query}
        
        System data: {data}
        
        Generate concise response. No filler. Direct answer only.
        """
        
        response = requests.post(
            f"{self.base_url}/chat",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            },
            json={"message": prompt}
        )
        
        return response.json()['response']
