"""
Run Anomaly Detection on Demo Data
This script analyzes all transactions and detects anomalies
"""
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.database import Database
from app.intelligence.anomaly_detector import AnomalyDetector

def run_anomaly_detection():
    print("=" * 60)
    print("RUNNING ANOMALY DETECTION")
    print("=" * 60)
    
    # Initialize
    db = Database('finance.db')
    detector = AnomalyDetector(db)
    
    # Run detection for user 1
    print("\nAnalyzing transactions for User ID: 1...")
    anomalies = detector.detect_anomalies(user_id=1)
    
    print("\n[OK] Detection Complete!")
    print(f"Found {len(anomalies)} anomalies")
    
    if anomalies:
        print("\nDetected Anomalies:")
        print("-" * 60)
        for i, anomaly in enumerate(anomalies, 1):
            print(f"\n{i}. Date: {anomaly['date']}")
            print(f"   Category: {anomaly['category']}")
            print(f"   Amount: Rs.{anomaly['amount']:.2f}")
            print(f"   Score: {anomaly['anomaly_score']:.3f}")
            print(f"   Reason: {anomaly['reason']}")
    else:
        print("\nNo anomalies detected.")
    
    print("\n" + "=" * 60)
    print("ANOMALY DETECTION COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    run_anomaly_detection()
