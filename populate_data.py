from app.models.database import Database
import random
from datetime import datetime, timedelta

def populate_demo_data():
    db = Database('finance.db')
    
    # 1. Create Demo User
    user_id = db.add_user('demo_user', 'demo@example.com')
    print(f"User ID: {user_id}")

    # 2. Add Monthly Income (Income)
    # Salary for past 3 months
    for i in range(3):
        date = (datetime.now() - timedelta(days=30*i)).strftime('%Y-%m-%d')
        db.add_transaction(user_id, date, 50000, 'Income', 'income', 'Salary', 'Job')
    
    # 3. Add Regular Expenses (Food, Transport, Utilities)
    categories = ['Food', 'Transport', 'Utilities', 'Entertainment', 'Health']
    
    # Last 60 days
    for i in range(60):
        # Add 1-2 transactions per day
        num_txn = random.randint(1, 2)
        for _ in range(num_txn):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            category = random.choice(categories)
            
            # Weighted amounts
            if category == 'Food':
                amount = random.randint(100, 800)
            elif category == 'Transport':
                amount = random.randint(50, 300)
            elif category == 'Utilities':
                amount = random.randint(500, 2000) if i % 30 == 0 else 0 # Monthly bills
            elif category == 'Entertainment':
                amount = random.randint(200, 1500)
            else:
                amount = random.randint(500, 5000)
                
            if amount > 0:
                db.add_transaction(user_id, date, amount, category, 'expense', f'{category} expense')

    # 4. Add some Anomalies (Weird high spending)
    # A party a week ago
    db.add_transaction(user_id, (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), 12000, 'Entertainment', 'expense', 'Big Party', 'Bar')
    
    # A medical emergency 20 days ago
    db.add_transaction(user_id, (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d'), 15000, 'Health', 'expense', 'Emergency', 'Hospital')

    # 5. Add Goals
    db.add_financial_goal(user_id, 'New Laptop', 80000, '2026-06-01')
    db.add_financial_goal(user_id, 'Bali Trip', 50000, '2026-12-01')
    
    print("Demo data populated successfully!")

if __name__ == '__main__':
    populate_demo_data()
