"""
Test Gemini AI Integration
Quick test to verify Gemini API is working with your financial data
"""
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from app.models.database import Database
from app.routes.chat import get_user_financial_context, build_financial_prompt
import google.generativeai as genai

def test_gemini():
    print("=" * 60)
    print("TESTING GEMINI AI INTEGRATION")
    print("=" * 60)
    
    # Check API key
    api_key = os.environ.get('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
    
    if api_key == 'YOUR_GEMINI_API_KEY_HERE':
        print("\n❌ ERROR: Gemini API key not set!")
        print("\nPlease set your API key:")
        print("  Windows: $env:GEMINI_API_KEY=\"your-key-here\"")
        print("  Linux/Mac: export GEMINI_API_KEY=\"your-key-here\"")
        print("\nOr create a .env file in the backend directory")
        print("\nGet your key from: https://makersuite.google.com/app/apikey")
        return
    
    print(f"\n✓ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        print("✓ Gemini model initialized")
    except Exception as e:
        print(f"\n❌ ERROR initializing Gemini: {e}")
        return
    
    # Get user context
    print("\n[1/3] Loading financial data...")
    db = Database('finance.db')
    context = get_user_financial_context(user_id=1)
    
    print(f"  - Transactions: {context['total_transactions']}")
    print(f"  - Balance: Rs.{context['current_balance']:,.2f}")
    print(f"  - Total Expenses: Rs.{context['total_expenses']:,.2f}")
    print(f"  - Anomalies: {context['anomaly_count']}")
    
    # Build prompt
    print("\n[2/3] Building context-aware prompt...")
    system_prompt = build_financial_prompt(context)
    print(f"  - Prompt length: {len(system_prompt)} characters")
    
    # Test questions
    test_questions = [
        "What's my current balance?",
        "Which category do I spend the most on?",
        "Give me one tip to save money"
    ]
    
    print("\n[3/3] Testing AI responses...")
    print("-" * 60)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        
        try:
            full_prompt = f"{system_prompt}\n\nUser Question: {question}\n\nProvide a helpful, concise response:"
            response = model.generate_content(full_prompt)
            print(f"   Answer: {response.text}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("GEMINI AI TEST COMPLETE!")
    print("=" * 60)
    print("\n✓ If you see responses above, Gemini is working!")
    print("✓ You can now use the AI Assistant in the app")
    print("\nNext: Start the app with 'python backend\\run.py'")

if __name__ == '__main__':
    test_gemini()
