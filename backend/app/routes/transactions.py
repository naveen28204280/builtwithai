from flask import Blueprint, request, jsonify, current_app

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('', methods=['POST'])
def add_transaction():
    """Add new transaction"""
    data = request.json
    
    required = ['user_id', 'date', 'amount', 'category', 'type']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields: user_id, date, amount, category, type'}), 400
    
    try:
        txn_id = current_app.db.add_transaction(
            user_id=data['user_id'],
            date=data['date'],
            amount=data['amount'],
            category=data['category'],
            txn_type=data['type'],
            description=data.get('description', ''),
            source=data.get('source', '')
        )
        return jsonify({
            'id': txn_id,
            'status': 'success',
            'message': 'Transaction added successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:user_id>', methods=['GET'])
def get_user_transactions(user_id):
    """Get all transactions for a user"""
    try:
        df = current_app.db.get_user_transactions(user_id)
        
        if df.empty:
            return jsonify({
                'user_id': user_id,
                'transactions': [],
                'count': 0
            }), 200
        
        transactions = df.to_dict('records')
        
        return jsonify({
            'user_id': user_id,
            'transactions': transactions,
            'count': len(transactions)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/<int:transaction_id>', methods=['DELETE'])
def delete_transaction(transaction_id):
    """Delete a transaction by ID"""
    try:
        conn = current_app.db.get_connection()
        cursor = conn.cursor()
        
        # Check if transaction exists
        cursor.execute('SELECT id, user_id FROM transactions WHERE id = ?', (transaction_id,))
        transaction = cursor.fetchone()
        
        if not transaction:
            conn.close()
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Delete transaction
        cursor.execute('DELETE FROM transactions WHERE id = ?', (transaction_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'id': transaction_id,
            'status': 'success',
            'message': 'Transaction deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/balance/<int:user_id>', methods=['GET'])
def get_balance(user_id):
    """Get user balance"""
    try:
        balance = current_app.db.get_user_balance(user_id)
        return jsonify({
            'user_id': user_id,
            'balance': balance
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transactions_bp.route('/categories/<int:user_id>', methods=['GET'])
def get_categories(user_id):
    """Get all categories for a user"""
    try:
        categories = current_app.db.get_all_categories(user_id)
        return jsonify({
            'user_id': user_id,
            'categories': categories
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
