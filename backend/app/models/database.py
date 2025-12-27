import sqlite3
import os
import pandas as pd
from datetime import datetime

class Database:
    def __init__(self, db_path='finance.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Check if database exists, create if not"""
        db_exists = os.path.exists(self.db_path)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if not db_exists:
            print(f"Database not found. Creating new database at {self.db_path}")
            self._create_tables(cursor)
            conn.commit()
            print("Database created successfully")
        else:
            print(f"Database found at {self.db_path}")
            # Verify tables exist, create if missing
            self._verify_tables(cursor)
            conn.commit()
        
        conn.close()
    
    def _create_tables(self, cursor):
        """Create all required tables"""
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Transactions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date DATE NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                type TEXT CHECK(type IN ('income', 'expense')) NOT NULL,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Financial goals table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS financial_goals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                goal_name TEXT NOT NULL,
                target_amount REAL NOT NULL,
                current_amount REAL DEFAULT 0,
                deadline DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Anomalies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS anomalies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                transaction_id INTEGER NOT NULL,
                detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                anomaly_score REAL NOT NULL,
                reason TEXT,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id)
            )
        ''')
        
        # Create indexes
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_user_date 
            ON transactions(user_id, date)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_transactions_category 
            ON transactions(category)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_anomalies_transaction 
            ON anomalies(transaction_id)
        ''')
        
        print("Tables created: users, transactions, financial_goals, anomalies")
    
    def _verify_tables(self, cursor):
        """Verify all tables exist, create missing ones"""
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' 
            AND name IN ('users', 'transactions', 'financial_goals', 'anomalies')
        """)
        
        existing_tables = {row[0] for row in cursor.fetchall()}
        required_tables = {'users', 'transactions', 'financial_goals', 'anomalies'}
        
        missing_tables = required_tables - existing_tables
        
        if missing_tables:
            print(f"Missing tables: {missing_tables}. Creating...")
            self._create_tables(cursor)
        else:
            print("All tables verified")
    
    def get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def add_user(self, username, email):
        """Add new user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO users (username, email)
                VALUES (?, ?)
            ''', (username, email))
            conn.commit()
            user_id = cursor.lastrowid
            print(f"User created: {username} (ID: {user_id})")
            return user_id
        except sqlite3.IntegrityError:
            print(f"User {username} already exists")
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def add_transaction(self, user_id, date, amount, category, txn_type, description='', source=''):
        """Add transaction"""
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
    
    def get_user_transactions(self, user_id, start_date=None, end_date=None, category=None):
        """Get user transactions with optional filters"""
        conn = self.get_connection()
        query = 'SELECT * FROM transactions WHERE user_id = ?'
        params = [user_id]
        
        if start_date:
            query += ' AND date >= ?'
            params.append(start_date)
        if end_date:
            query += ' AND date <= ?'
            params.append(end_date)
        if category:
            query += ' AND category = ?'
            params.append(category)
        
        query += ' ORDER BY date DESC'
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    def get_all_categories(self, user_id):
        """Get all unique categories for user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT category FROM transactions 
            WHERE user_id = ?
        ''', (user_id,))
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories
    
    def get_user_balance(self, user_id):
        """Calculate current balance"""
        df = self.get_user_transactions(user_id)
        if df.empty:
            return 0
        
        income = df[df['type'] == 'income']['amount'].sum()
        expenses = df[df['type'] == 'expense']['amount'].sum()
        return income - expenses
    
    def log_anomaly(self, transaction_id, score, reason):
        """Log detected anomaly"""
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