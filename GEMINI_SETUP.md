# 🤖 Gemini AI Assistant Setup Guide

## Overview

The Finance AI application now uses **Google's Gemini API** for the AI Assistant feature. This provides intelligent, context-aware financial advice based on your actual transaction data.

---

## 🔑 Getting Your Gemini API Key

### Step 1: Visit Google AI Studio
Go to: **https://makersuite.google.com/app/apikey**

### Step 2: Sign in with Google Account
- Use your Google account to sign in
- Accept the terms of service

### Step 3: Create API Key
1. Click **"Create API Key"**
2. Select a Google Cloud project (or create a new one)
3. Copy the generated API key
4. **Keep it safe!** Don't share it publicly

---

## ⚙️ Configuring the Application

### Option 1: Environment Variable (Recommended)

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GEMINI_API_KEY="your-api-key-here"
```

### Option 2: .env File

1. Create a file named `.env` in the `backend` directory
2. Add this line:
```
GEMINI_API_KEY=your-api-key-here
```

### Option 3: Direct Code Edit (Not Recommended for Production)

Edit `backend/app/routes/chat.py` line 18:
```python
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'paste-your-key-here')
```

---

## 🧪 Testing the AI Assistant

### 1. Start the Backend
```bash
python backend\run.py
```

### 2. Open the Frontend
```bash
start frontend\index.html
```

### 3. Navigate to AI Assistant Tab
Click on the "AI Assistant" tab in the navigation

### 4. Try These Questions:
- "How much did I spend on food?"
- "What's my current balance?"
- "Which category do I spend the most on?"
- "Give me advice on reducing my expenses"
- "How many anomalies were detected?"
- "What are my financial goals?"

---

## 🎯 What the AI Can Do

### Context-Aware Responses
The AI has access to:
- ✅ Your current balance
- ✅ Total income and expenses
- ✅ Spending breakdown by category
- ✅ Recent transaction activity (last 7 days)
- ✅ Number of detected anomalies
- ✅ Active financial goals count

### Example Interactions

**You:** "How much did I spend on food?"
**AI:** "Based on your transactions, you've spent Rs.X,XXX on Food. This is your [2nd/3rd] highest spending category. Consider meal planning to reduce costs!"

**You:** "What's my biggest expense?"
**AI:** "Your top spending category is [Category] with Rs.X,XXX spent. This accounts for XX% of your total expenses."

**You:** "Give me financial advice"
**AI:** "With a balance of Rs.X,XXX and [positive/negative] cash flow, I recommend [specific advice based on your data]."

---

## 🔒 API Key Security

### ✅ DO:
- Store API key in environment variables
- Use `.env` file (add to `.gitignore`)
- Keep your key private
- Rotate keys periodically

### ❌ DON'T:
- Commit API keys to Git
- Share keys publicly
- Hardcode keys in production
- Use the same key across multiple projects

---

## 💰 Pricing & Limits

### Gemini API Free Tier:
- **60 requests per minute**
- **1,500 requests per day**
- **1 million tokens per month**

This is **more than enough** for a student finance app demo!

### For Production:
- Consider upgrading to paid tier
- Implement rate limiting
- Add caching for common queries

---

## 🐛 Troubleshooting

### Error: "API key not found"
**Solution:** Set the `GEMINI_API_KEY` environment variable

### Error: "API key invalid"
**Solution:** 
1. Check if you copied the full key
2. Generate a new key from Google AI Studio
3. Make sure there are no extra spaces

### Error: "Quota exceeded"
**Solution:**
- Wait for the quota to reset (daily/monthly)
- Reduce request frequency
- Upgrade to paid tier

### AI gives generic responses
**Solution:**
- Make sure backend is running
- Check that database has transactions
- Verify API key is set correctly

---

## 🔄 Fallback Behavior

If Gemini API fails:
- App shows a friendly error message
- User can still use other features
- No crash or data loss

---

## 📊 Data Privacy

### What data is sent to Gemini?
- **Summary statistics only** (totals, counts, categories)
- **NO individual transaction details**
- **NO personal information**
- **NO sensitive data**

### Example of data sent:
```
Current Balance: Rs.50,000
Total Expenses: Rs.100,000
Top Category: Food (Rs.30,000)
Anomalies: 5
```

---

## 🚀 Next Steps

1. **Get your API key** from Google AI Studio
2. **Set the environment variable** or create `.env` file
3. **Restart the backend** to load the new key
4. **Test the AI Assistant** with sample questions
5. **Enjoy intelligent financial advice!**

---

## 📞 Support

### Gemini API Documentation:
https://ai.google.dev/docs

### Google AI Studio:
https://makersuite.google.com/

### Issues?
Check the console logs in:
- Backend terminal (for API errors)
- Browser console (for frontend errors)

---

**🎉 Your AI Assistant is ready to help with financial decisions!**
