# Free Cloud Database Setup Guide for FitFoodie

## Option 1: Railway (Recommended - Easiest)

Railway offers a free MySQL database with no credit card required.

### Step 1: Create Railway Account
1. Go to https://railway.app
2. Click **"Start a New Project"**
3. Sign up with GitHub (free, no credit card needed)

### Step 2: Create MySQL Database
1. After logging in, click **"New Project"**
2. Select **"Provision MySQL"**
3. Wait for the database to be created (takes ~30 seconds)

### Step 3: Get Connection Details
1. Click on your MySQL database
2. Go to the **"Variables"** tab
3. You'll see these variables:
   - `MYSQL_HOST` (looks like: `containers-us-west-xxx.railway.app`)
   - `MYSQL_PORT` (usually `3306`)
   - `MYSQL_USER` (usually `root`)
   - `MYSQL_PASSWORD` (a long random string)
   - `MYSQL_DATABASE` (database name)

### Step 4: Import Your Schema
1. In Railway, go to the **"Data"** tab
2. Click **"Query"**
3. Copy and paste the contents of `trio/schema.sql`
4. Click **"Execute"**

OR use a MySQL client:
```bash
mysql -h [MYSQL_HOST] -u [MYSQL_USER] -p[MYSQL_PASSWORD] [MYSQL_DATABASE] < trio/schema.sql
```

### Step 5: Add to Vercel
1. Go to Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add these variables:

```
MYSQL_HOST = [your Railway host]
MYSQL_USER = [your Railway user]
MYSQL_PASSWORD = [your Railway password]
MYSQL_DB = [your Railway database name]
```

3. Click **Save**
4. Go to **Deployments** tab → Click **"Redeploy"**

---

## Option 2: Neon (PostgreSQL - Also Free)

If you prefer PostgreSQL over MySQL:

### Step 1: Create Neon Account
1. Go to https://neon.tech
2. Sign up with GitHub (free, no credit card)

### Step 2: Create Database
1. Click **"Create Project"**
2. Choose a region close to you
3. Wait for creation

### Step 3: Get Connection String
1. Click **"Connection Details"**
2. Copy the connection string

**Note:** You'll need to modify your app to use PostgreSQL instead of MySQL (different library: `psycopg2` instead of `pymysql`)

---

## Option 3: PlanetScale (MySQL)

PlanetScale is great but requires more setup.

### Step 1: Create Account
1. Go to https://planetscale.com
2. Sign up (free tier available)

### Step 2: Create Database
1. Click **"Create database"**
2. Choose a name
3. Select a region

### Step 3: Get Credentials
1. Click **"Connect"**
2. Select **"General"**
3. Copy the connection details

---

## ⚡ Quick Start (Railway - Recommended)

I recommend **Railway** because:
- ✅ No credit card required
- ✅ MySQL (same as your local setup)
- ✅ Easy to use
- ✅ Free tier is generous
- ✅ Can import schema directly

**Total time: ~5 minutes**

---

## After Setup

Once you've added the environment variables to Vercel:

1. Go to Vercel → Deployments → Redeploy
2. Wait for deployment to finish
3. Visit `your-vercel-url/status` to verify database connection
4. You should see: **Database: ✅ Connected**
5. Now login/register will work!

---

## Need Help?

Let me know which option you choose and I can help you with the specific steps!
