# 🔑 Get Your Gemini API Key - Step by Step

## Quick Link
👉 **https://makersuite.google.com/app/apikey**

---

## Step-by-Step Instructions

### Step 1: Open Google AI Studio
1. Open your browser
2. Go to: **https://makersuite.google.com/app/apikey**
3. You'll see the Google AI Studio page

### Step 2: Sign In
1. Click "Sign in with Google"
2. Use your Google account (Gmail)
3. Accept the terms of service if prompted

### Step 3: Create API Key
1. You'll see a button: **"Create API Key"**
2. Click it
3. A dialog will appear

### Step 4: Select Project
1. Choose "Create API key in new project" (recommended)
   - OR select an existing Google Cloud project
2. Click "Create"

### Step 5: Copy Your Key
1. Your API key will be displayed
2. It looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`
3. Click the **copy icon** to copy it
4. **IMPORTANT**: Save it somewhere safe!

---

## Setting Up the API Key

### Windows (PowerShell) - Recommended
```powershell
# Open PowerShell and run:
$env:GEMINI_API_KEY="paste-your-key-here"

# Verify it's set:
echo $env:GEMINI_API_KEY
```

### Windows (Command Prompt)
```cmd
set GEMINI_API_KEY=paste-your-key-here
```

### Create .env File (Alternative)
1. Navigate to the `backend` folder
2. Create a new file named `.env`
3. Add this line:
```
GEMINI_API_KEY=paste-your-key-here
```
4. Save the file

---

## Testing Your Setup

### Quick Test
```bash
# Run the test script
python test_gemini.py
```

### Expected Output:
```
============================================================
TESTING GEMINI AI INTEGRATION
============================================================

✓ API Key found: AIzaSyXXXX...XXXX
✓ Gemini model initialized

[1/3] Loading financial data...
  - Transactions: 281
  - Balance: Rs.-180,798.92
  - Total Expenses: Rs.425,798.92
  - Anomalies: 28

[2/3] Building context-aware prompt...
  - Prompt length: XXXX characters

[3/3] Testing AI responses...
------------------------------------------------------------

1. Question: What's my current balance?
   Answer: [AI response about your balance]

2. Question: Which category do I spend the most on?
   Answer: [AI response about top category]

3. Question: Give me one tip to save money
   Answer: [AI response with saving tip]

============================================================
GEMINI AI TEST COMPLETE!
============================================================

✓ If you see responses above, Gemini is working!
✓ You can now use the AI Assistant in the app
```

---

## Common Issues

### ❌ "API key not found"
**Solution:**
- Make sure you set the environment variable
- Restart your terminal/PowerShell
- Try the .env file method instead

### ❌ "Invalid API key"
**Solution:**
- Check you copied the entire key
- Make sure there are no extra spaces
- Generate a new key and try again

### ❌ "Quota exceeded"
**Solution:**
- You've hit the free tier limit
- Wait 24 hours for reset
- Or upgrade to paid tier

---

## Free Tier Limits

✅ **60 requests per minute**
✅ **1,500 requests per day**
✅ **1 million tokens per month**

This is **plenty** for:
- Development
- Testing
- Demos
- Student projects

---

## Security Tips

### ✅ DO:
- Store key in environment variables
- Use .env file (add to .gitignore)
- Keep your key private
- Rotate keys periodically

### ❌ DON'T:
- Commit keys to Git
- Share keys publicly
- Hardcode in source code
- Use same key everywhere

---

## Ready to Go!

Once you see the test output:
1. ✅ Your API key is working
2. ✅ Gemini is connected
3. ✅ Financial data is loaded
4. ✅ AI responses are working

**Next:** Start the app and try the AI Assistant!

```bash
# Start backend
python backend\run.py

# Open frontend
start frontend\index.html
```

---

## Need Help?

- **Gemini Docs**: https://ai.google.dev/docs
- **API Studio**: https://makersuite.google.com/
- **Pricing Info**: https://ai.google.dev/pricing

---

**🎉 You're all set! Enjoy your AI-powered financial assistant!**
