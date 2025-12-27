from prophet import Prophet
import pandas as pd
from datetime import datetime, timedelta

class ExpenseForecaster:
    def __init__(self, db):
        self.db = db
    
    def forecast_expenses(self, user_id, days_ahead=30, category=None):
        # Get historical data
        df = self.db.get_user_transactions(user_id)
        
        if category:
            df = df[df['category'] == category]
        
        # Filter expenses only
        df = df[df['type'] == 'expense']
        
        # Prepare for Prophet
        df_prophet = df.groupby('date').agg({'amount': 'sum'}).reset_index()
        df_prophet.columns = ['ds', 'y']
        df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
        
        # Train Prophet
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=False
        )
        model.fit(df_prophet)
        
        # Forecast
        future = model.make_future_dataframe(periods=days_ahead)
        forecast = model.predict(future)
        
        # Extract future predictions
        future_forecast = forecast[forecast['ds'] > df_prophet['ds'].max()]
        
        return {
            'dates': future_forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
            'predicted_amount': future_forecast['yhat'].tolist(),
            'lower_bound': future_forecast['yhat_lower'].tolist(),
            'upper_bound': future_forecast['yhat_upper'].tolist(),
            'total_predicted': future_forecast['yhat'].sum()
        }
    
    def get_spending_trends(self, user_id):
        df = self.db.get_user_transactions(user_id)
        df = df[df['type'] == 'expense']
        df['date'] = pd.to_datetime(df['date'])
        
        # Category-wise trends
        category_trends = df.groupby(['category', pd.Grouper(key='date', freq='W')])['amount'].sum().reset_index()
        
        return category_trends.to_dict('records')
