# Railway MySQL Setup - Step by Step Guide

## 📍 STEP 1: Login to Railway
1. Go to https://railway.app (already open in your browser)
2. Click **"Login"** button (top right)
3. Click **"Login with GitHub"**
4. Authorize Railway
5. You'll see the Railway Dashboard

---

## 📍 STEP 2: Create New Project
1. On the Railway Dashboard, click **"New Project"** button
2. You'll see several options:
   - Deploy from GitHub repo
   - **Provision MySQL** ← Click this one!
   - Provision PostgreSQL
   - Provision Redis
   - Empty Project

---

## 📍 STEP 3: Wait for MySQL to Deploy
1. Railway will create your MySQL database
2. Wait ~30 seconds
3. You'll see a card labeled **"MySQL"**

---

## 📍 STEP 4: Get Connection Details
1. Click on the **MySQL** card
2. Click on the **"Variables"** tab
3. You'll see these variables - COPY THEM:
   ```
   MYSQLHOST = containers-us-west-xxx.railway.app
   MYSQLPORT = 3306
   MYSQLUSER = root
   MYSQLPASSWORD = [long random string]
   MYSQLDATABASE = railway
   ```

---

## 📍 STEP 5: Import Schema
1. In the MySQL card, click **"Data"** tab
2. Click **"Query"** button
3. Open the file: `railway_schema.sql` (I created it for you)
4. Copy ALL the contents
5. Paste into Railway's Query editor
6. Click **"Run"** or **"Execute"**
7. You should see: "Query executed successfully"

---

## 📍 STEP 6: Add to Vercel
1. Go to https://vercel.com/dashboard
2. Click on your **FitFoodie** project
3. Click **"Settings"** tab
4. Click **"Environment Variables"**
5. Add these 4 variables (use values from Railway Step 4):

   **Variable 1:**
   - Key: `MYSQL_HOST`
   - Value: [your MYSQLHOST from Railway]
   - Environment: Production, Preview, Development (all three)
   
   **Variable 2:**
   - Key: `MYSQL_USER`
   - Value: [your MYSQLUSER from Railway]
   - Environment: Production, Preview, Development
   
   **Variable 3:**
   - Key: `MYSQL_PASSWORD`
   - Value: [your MYSQLPASSWORD from Railway]
   - Environment: Production, Preview, Development
   
   **Variable 4:**
   - Key: `MYSQL_DB`
   - Value: [your MYSQLDATABASE from Railway]
   - Environment: Production, Preview, Development

6. Click **"Save"** for each variable

---

## 📍 STEP 7: Redeploy on Vercel
1. Go to **"Deployments"** tab
2. Click the **three dots (•••)** on the latest deployment
3. Click **"Redeploy"**
4. Wait for deployment to complete (~1 minute)

---

## 📍 STEP 8: Test It!
1. Visit your Vercel URL
2. Go to `/status` page (e.g., `your-app.vercel.app/status`)
3. You should see: **Database: ✅ Connected**
4. Now try to register/login - it should work!

---

## ❓ Troubleshooting

**Can't find "Provision MySQL"?**
- Make sure you clicked "New Project" first
- Look for a database icon with "MySQL" label

**Schema import failed?**
- Make sure you copied the ENTIRE contents of `railway_schema.sql`
- Check for any error messages in Railway

**Vercel still shows database error?**
- Double-check you added all 4 environment variables
- Make sure you clicked "Save" for each one
- Make sure you redeployed after adding variables

---

## 🎉 Success!
Once you see "Database: ✅ Connected" on the `/status` page, your app is fully working with:
- ✅ Login/Register
- ✅ Profile page
- ✅ Cloud database
- ✅ Deployed on Vercel

---

**Current Step:** Tell me which step you're on and I'll help you!
