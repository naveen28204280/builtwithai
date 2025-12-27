import sqlite3
from datetime import datetime
import pandas as pd

class Database:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def add_transaction(self, user_id, date, amount, category, txn_type, description='', source=''):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (user_id, date, amount, category, type, description, source)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, date, amount, category, txn_type, description, source))
        conn.commit()
        txn_id = cursor.lastrowid
        conn.close()
        return txn_id
    
    def get_user_transactions(self, user_id, start_date=None, end_date=None):
        conn = self.get_connection()
        query = 'SELECT * FROM transactions WHERE user_id = ?'
        params = [user_id]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        
        query += ' ORDER BY date DESC'
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def log_anomaly(self, transaction_id, score, reason):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO anomalies (transaction_id, anomaly_score, reason)
            VALUES (?, ?, ?)
        ''', (transaction_id, score, reason))
        conn.commit()
        conn.close()
        def get_anomalies(self, user_id, limit=10):
        """Get recent anomalies for user"""
        conn = self.get_connection()
        query = '''
            SELECT a.*, t.date, t.amount, t.category 
            FROM anomalies a
            JOIN transactions t ON a.transaction_id = t.id
            WHERE t.user_id = ?
            ORDER BY a.detected_at DESC
            LIMIT ?
        '''
        df = pd.read_sql_query(query, conn, params=(user_id, limit))
        conn.close()
        return df
    
    def add_financial_goal(self, user_id, goal_name, target_amount, deadline=None):
        """Add financial goal"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO financial_goals (user_id, goal_name, target_amount, deadline)
            VALUES (?, ?, ?, ?)
        ''', (user_id, goal_name, target_amount, deadline))
        conn.commit()
        goal_id = cursor.lastrowid
        conn.close()
        return goal_id
    
    def get_user_goals(self, user_id):
        """Get all goals for user"""
        conn = self.get_connection()
        query = 'SELECT * FROM financial_goals WHERE user_id = ?'
        df = pd.read_sql_query(query, conn, params=(user_id,))
        conn.close()
        return df
    
    def reset_database(self):
        """Delete and recreate database - USE CAREFULLY"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
            print(f"Database {self.db_path} deleted")
        self.init_db()
