# Quick 5-Minute Deployment - External Database

## Step 1: Create Free MySQL Database (2 minutes)

Go to **https://aiven.io/mysql**
1. Click "Start Free"
2. Sign up with Google/GitHub
3. Create a MySQL service:
   - Choose **"MySQL"**
   - Select **"Free plan"** (no credit card needed)
   - Choose region closest to you
   - Click "Create service"

## Step 2: Get Connection Details (1 minute)

Once created, Aiven will show:
- **Host**: `mysql-xxxxx.aivencloud.com`
- **Port**: `12345`
- **User**: `avnadmin`
- **Password**: `xxxxxxxxx`
- **Database**: `defaultdb`

## Step 3: Add to Railway (1 minute)

In Railway, go to your web service → Variables:

Add ONE variable:
```
DATABASE_URL=mysql://avnadmin:YOUR_PASSWORD@mysql-xxxxx.aivencloud.com:12345/defaultdb
```

(Replace with your actual Aiven credentials)

## Step 4: Update Code (1 minute - I'll do this)

I'll update the code to use `DATABASE_URL` instead of separate variables.

## Step 5: Deploy! (30 seconds)

Railway will auto-redeploy and your app will be LIVE!

---

**Total time: 5 minutes**
**Cost: $0 (completely free)**
