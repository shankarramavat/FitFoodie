# Railway Deployment Steps

## Quick Deploy (5 minutes)

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign in with GitHub

### Step 2: Deploy from GitHub
1. Click "Deploy from GitHub repo"
2. Select `shankarramavat/FitFoodie`
3. Railway will automatically detect it's a Python app

### Step 3: Add MySQL Database
1. In your Railway project, click "New"
2. Select "Database" → "MySQL"
3. Railway will create a database and provide credentials

### Step 4: Set Environment Variables
Click on your web service → "Variables" → Add these:

```
FLASK_SECRET_KEY=your_secret_key_here
CLARIFAI_API_KEY=your_clarifai_key
WOLFRAM_APP_ID=your_wolfram_id
```

The MySQL variables will be automatically set by Railway!

### Step 5: Deploy!
1. Click "Deploy"
2. Wait 2-3 minutes
3. Railway will give you a public URL like: `https://fitfoodie-production.up.railway.app`

## That's it! Your app will be live with ALL features working.

## Cost
- **Free tier**: 500 hours/month (enough for testing)
- **Paid**: $5/month for unlimited usage

## Need Help?
If you get stuck, copy the error from Railway logs and I'll fix it immediately.
