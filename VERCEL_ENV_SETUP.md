# Vercel Environment Variables Setup Guide

## How to Add Environment Variables in Vercel

1. Go to your Vercel Dashboard: https://vercel.com/dashboard
2. Click on your **FitFoodie** project
3. Click on **Settings** tab
4. Click on **Environment Variables** in the left sidebar
5. For each variable below, click **Add New** and enter:
   - **Key** (variable name)
   - **Value** (the value shown below)
   - **Environment**: Select **Production**, **Preview**, and **Development** (all three)
6. Click **Save**

---

## Environment Variables to Add

Copy and paste these **exactly** as shown:

### 1. FLASK_SECRET_KEY
```
Key:   FLASK_SECRET_KEY
Value: xyz623
```

### 2. MYSQL_HOST
```
Key:   MYSQL_HOST
Value: localhost
```
**⚠️ IMPORTANT**: If you're using a cloud database (like PlanetScale, Railway, or AWS RDS), replace `localhost` with your actual database host URL.

### 3. MYSQL_USER
```
Key:   MYSQL_USER
Value: root
```
**⚠️ IMPORTANT**: If you're using a cloud database, replace `root` with your actual database username.

### 4. MYSQL_PASSWORD
```
Key:   MYSQL_PASSWORD
Value: root
```
**⚠️ IMPORTANT**: If you're using a cloud database, replace `root` with your actual database password.

### 5. MYSQL_DB
```
Key:   MYSQL_DB
Value: geeklogin
```
**⚠️ IMPORTANT**: If you're using a cloud database, replace `geeklogin` with your actual database name.

### 6. CLARIFAI_API_KEY
```
Key:   CLARIFAI_API_KEY
Value: 973f24ce16744a039a4e351a96a61fc0
```

### 7. WOLFRAM_APP_ID
```
Key:   WOLFRAM_APP_ID
Value: E22T3V-XRQPTQAVQX
```

---

## ⚠️ CRITICAL: Database Configuration

**Your current MySQL settings use `localhost` which will NOT work on Vercel!**

Vercel is a serverless platform and cannot connect to a local MySQL database. You have two options:

### Option A: Use a Cloud Database (Recommended)
Use a free cloud MySQL/PostgreSQL service:
- **PlanetScale** (MySQL) - Free tier available
- **Railway** - Free tier available
- **Neon** (PostgreSQL) - Free tier available
- **Supabase** (PostgreSQL) - Free tier available

Once you set up a cloud database:
1. Update the `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DB` values above
2. Import your schema using the `trio/schema.sql` file

### Option B: Disable Database Features (Quick Test)
If you just want to test the deployment without database functionality:
- The app will still crash when you try to login/register
- But the home page should load

---

## After Adding Variables

1. Go back to your Vercel project **Deployments** tab
2. Click the **three dots** (•••) on the latest deployment
3. Click **Redeploy**
4. Wait for the deployment to complete
5. Visit your Vercel URL to test

---

## Quick Copy-Paste Format (for advanced users)

If Vercel supports bulk import, you can use this format:

```env
FLASK_SECRET_KEY=xyz623
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=root
MYSQL_DB=geeklogin
CLARIFAI_API_KEY=973f24ce16744a039a4e351a96a61fc0
WOLFRAM_APP_ID=E22T3V-XRQPTQAVQX
```

**Remember to replace the MySQL values with your cloud database credentials!**
