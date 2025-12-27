from sklearn.ensemble import IsolationForest
import numpy as np
import pandas as pd

class AnomalyDetector:
    def __init__(self, db):
        self.db = db
        self.model = IsolationForest(contamination=0.1, random_state=42)
    
    def detect_anomalies(self, user_id):
        df = self.db.get_user_transactions(user_id)
        df = df[df['type'] == 'expense']
        
        if len(df) < 10:
            return []
        
        # Feature engineering
        df['day_of_week'] = pd.to_datetime(df['date']).dt.dayofweek
        df['day_of_month'] = pd.to_datetime(df['date']).dt.day
        
        # Category encoding
        category_map = {cat: idx for idx, cat in enumerate(df['category'].unique())}
        df['category_encoded'] = df['category'].map(category_map)
        
        # Features for anomaly detection
        features = df[['amount', 'day_of_week', 'category_encoded']].values
        
        # Fit and predict
        predictions = self.model.fit_predict(features)
        anomaly_scores = self.model.score_samples(features)
        
        # Flag anomalies
        df['is_anomaly'] = predictions == -1
        df['anomaly_score'] = anomaly_scores
        
        anomalies = df[df['is_anomaly']].copy()
        
        # Generate reasons
        for idx, row in anomalies.iterrows():
            reason = self._generate_reason(row, df)
            anomalies.at[idx, 'reason'] = reason
            
            # Log to database
            self.db.log_anomaly(row['id'], row['anomaly_score'], reason)
        
        return anomalies[['id', 'date', 'amount', 'category', 'anomaly_score', 'reason']].to_dict('records')
    
    def _generate_reason(self, transaction, history):
        category_avg = history[history['category'] == transaction['category']]['amount'].mean()
        overall_avg = history['amount'].mean()
        
        if transaction['amount'] > category_avg * 2:
            return f"Amount ${transaction['amount']:.2f} is {transaction['amount']/category_avg:.1f}x category average"
        elif transaction['amount'] > overall_avg * 3:
            return f"Unusually high spending: {transaction['amount']/overall_avg:.1f}x overall average"
        else:
            return "Unusual pattern detected"
