from flask import Blueprint, request, jsonify
from app.models.database import Database

transactions_bp = Blueprint('transactions', __name__)
db = Database()

@transactions_bp.route('/transactions', methods=['POST'])
def add_transaction():
    data = request.json
    txn_id = db.add_transaction(
        user_id=data['user_id'],
        date=data['date'],
        amount=data['amount'],
        category=data['category'],
        txn_type=data['type'],
        description=data.get('description', ''),
        source=data.get('source', '')
    )
    return jsonify({'id': txn_id, 'status': 'success'})

@transactions_bp.route('/transactions/<int:user_id>', methods=['GET'])
def get_transactions(user_id):
    df = db.get_user_transactions(user_id)
    return jsonify(df.to_dict('records'))
