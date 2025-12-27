from flask import Blueprint, request, jsonify
from app.models.database import Database
from app.intelligence.forecasting import ExpenseForecaster
from app.intelligence.anomaly_detector import AnomalyDetector
from app.utils.chatterbox_client import ChatterboxClient
import json

chat_bp = Blueprint('chat', __name__)

db = Database()
forecaster = ExpenseForecaster(db)
anomaly_detector = AnomalyDetector(db)
chatterbox = ChatterboxClient()

@chat_bp.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_id = data['user_id']
    message = data['message']
    
    # Get user context
    context = get_user_context(user_id)
    
    # Process with Chatterbox
    intent_data = chatterbox.process_query(message, context)
    
    try:
        intent_obj = json.loads(intent_data.get('response', '{}'))
    except:
        return jsonify({'error': 'Failed to parse intent'}), 400
    
    # Route based on intent
    intent = intent_obj.get('intent')
    
    if intent == 'forecast':
        days = intent_obj.get('time_range', 30)
        category = intent_obj.get('category')
        result = forecaster.forecast_expenses(user_id, days, category)
        
    elif intent == 'anomaly_check':
        result = anomaly_detector.detect_anomalies(user_id)
        
    elif intent == 'spending_summary':
        df = db.get_user_transactions(user_id)
        result = {
            'total_spent': df[df['type'] == 'expense']['amount'].sum(),
            'by_category': df[df['type'] == 'expense'].groupby('category')['amount'].sum().to_dict()
        }
    
    else:
        result = {'message': 'Intent not recognized'}
    
    # Generate natural language response
    response_text = chatterbox.generate_response(result, message)
    
    return jsonify({
        'intent': intent,
        'data': result,
        'response': response_text
    })

def get_user_context(user_id):
    df = db.get_user_transactions(user_id)
    return {
        'balance': df[df['type'] == 'income']['amount'].sum() - df[df['type'] == 'expense']['amount'].sum(),
        'monthly_spending': df[df['type'] == 'expense']['amount'].tail(30).sum(),
        'anomaly_count': len(anomaly_detector.detect_anomalies(user_id)),
        'categories': df['category'].unique().tolist()
    }
