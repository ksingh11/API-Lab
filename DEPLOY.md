# 🚀 Deployment Guide for Beginners

This guide will help you deploy API Zero to Hero to Render (free hosting) with zero DevOps experience needed.

---

## ✅ Pre-Deployment Checklist

Before deploying, make sure:

- [ ] You have a GitHub account (create one at https://github.com)
- [ ] You have pushed this code to a GitHub repository
- [ ] You have a Render account (free, no credit card needed)

---

## 📦 Option 1: One-Click Deploy to Render (Easiest!)

### Step 1: Click the Deploy Button

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

Or manually go to: https://render.com/deploy

### Step 2: Connect Your Repository

1. Sign in to Render (create account if needed)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your `apilab` repository
5. Click "Connect"

### Step 3: Configure (Use These Exact Settings)

Render will auto-detect most settings from `render.yaml`, but verify:

| Setting | Value | Notes |
|---------|-------|-------|
| **Name** | `apilab` or your choice | This will be your URL |
| **Region** | Oregon (US West) | Or closest to you |
| **Branch** | `main` or `master` | Your default branch |
| **Runtime** | Python 3 | Auto-detected |
| **Build Command** | `pip install -r requirements.txt` | Auto-filled from render.yaml |
| **Start Command** | `gunicorn wsgi:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1` | Auto-filled from render.yaml |
| **Plan** | **Free** | Select free tier |

### Step 4: Environment Variables (Auto-Configured!)

These are automatically set from `render.yaml`:

- ✅ `SECRET_KEY` - Auto-generated secure random value
- ✅ `JWT_SECRET_KEY` - Auto-generated secure random value  
- ✅ `DATABASE_URL` - `sqlite:///instance/apilab.db`
- ✅ `FLASK_ENV` - `production`
- ✅ `PYTHON_VERSION` - `3.11.7`

**You don't need to add anything manually!**

### Step 5: Add Persistent Disk (IMPORTANT!)

This ensures your database isn't deleted when the server restarts.

1. Scroll down to **Disks** section
2. Click "Add Disk"
3. Configure:
   - **Name**: `apilab-data`
   - **Mount Path**: `/opt/render/project/instance`
   - **Size**: `1 GB` (free tier limit)
4. Click "Create Disk"

### Step 6: Deploy!

1. Click **"Create Web Service"** button
2. Wait 2-3 minutes for deployment
3. Watch the logs - you should see:
   ```
   ==> Building...
   Installing dependencies from requirements.txt...
   ==> Build successful!
   ==> Starting server...
   ✅ Created instance directory
   ⚠️  Database is empty. Auto-seeding with default data...
   ✅ Database seeded successfully!
   ```

### Step 7: Test Your Deployment

1. Click the URL at the top (e.g., `https://apilab-xyz.onrender.com`)
2. You should see the API Zero to Hero dashboard
3. Try logging in:
   - Email: `testuser@apilab.dev`
   - Password: `test123`
4. Make a test request to `/api/todos`

---

## 🔧 Manual Deployment to Render (If Button Doesn't Work)

### Step 1: Create Web Service Manually

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Fill in the form with these values:

```yaml
Name: apilab
Region: Oregon (US West)
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn wsgi:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1
```

### Step 2: Add Environment Variables

Click "Advanced" → "Add Environment Variable" for each:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.7` |
| `FLASK_ENV` | `production` |
| `DATABASE_URL` | `sqlite:///instance/apilab.db` |

For `SECRET_KEY` and `JWT_SECRET_KEY`, click "Generate" to create random values.

### Step 3: Add Disk

Under "Disks" section:
- Name: `apilab-data`
- Mount Path: `/opt/render/project/instance`  
- Size: `1 GB`

### Step 4: Deploy

Click "Create Web Service" and wait for deployment.

---

## 🐛 Troubleshooting

### Issue: "Application failed to start"

**Solution:**
1. Check logs in Render dashboard
2. Look for errors in the build or start phase
3. Common fixes:
   - Make sure `requirements.txt` has all dependencies
   - Verify `gunicorn` is in `requirements.txt`
   - Check that `app.py` exists in root directory

### Issue: "Database resets on every restart"

**Solution:**
- Make sure you added the persistent disk
- Verify mount path is `/opt/render/project/instance`
- Check that `DATABASE_URL` env var points to `sqlite:///instance/apilab.db`

### Issue: "502 Bad Gateway" on first request

**Solution:**
- This is normal! Free tier apps sleep after 15 minutes
- First request takes ~30 seconds to wake up
- Just wait and refresh the page

### Issue: "Secret key not found"

**Solution:**
- Go to Render dashboard → Environment
- Add `SECRET_KEY` and `JWT_SECRET_KEY` with random values
- Or use the "Generate" button in Render UI

### Issue: Can't see database changes

**Solution:**
- Make sure persistent disk is mounted
- Check logs for "Created instance directory" message
- Verify database path in environment variables

---

## 📊 What Happens During Deployment?

Here's what Render does automatically:

1. **Clone your code** from GitHub
2. **Install Python 3.11.7** (from `runtime.txt`)
3. **Install dependencies** (from `requirements.txt`)
4. **Create instance folder** (from `app/__init__.py`)
5. **Initialize database** (SQLite, auto-created)
6. **Seed default data** (2 users + 6 todos)
7. **Start gunicorn** (binds to Render's assigned `$PORT`)
8. **Assign public URL** (e.g., `https://apilab-abc.onrender.com`)

---

## 🔒 Security Notes for Production

While this is a learning app, here are best practices:

- ✅ Secrets are auto-generated (not hardcoded)
- ✅ HTTPS is enforced by Render
- ✅ Environment variables are encrypted
- ⚠️  SQLite is fine for learning, but use PostgreSQL for real apps
- ⚠️  Free tier sleeps after 15 min - upgrade for 24/7 availability

---

## 💰 Cost Breakdown

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| **Render** | ✅ Free forever | $7/month (no sleep) |
| **Railway** | ✅ $5 free credit | $5/month usage-based |
| **Heroku** | ❌ No free tier | $7/month |

**Recommendation for beginners:** Start with Render's free tier!

---

## 🔄 Updating Your Deployment

After you push changes to GitHub:

1. Render auto-deploys on every push to `main` branch
2. Or manually click "Deploy latest commit" in Render dashboard
3. Wait 1-2 minutes for rebuild
4. Database data persists (thanks to disk mount)

---

## 📞 Need Help?

1. Check Render's logs: Dashboard → Your Service → Logs
2. Read error messages carefully (they're usually helpful!)
3. Search GitHub issues: https://github.com/yourusername/apilab/issues
4. Create a new issue with your error logs

---

## ✅ Deployment Success Checklist

After deployment, verify:

- [ ] Homepage loads at your Render URL
- [ ] You can click "Playground" tab
- [ ] Login works with `testuser@apilab.dev` / `test123`
- [ ] GET request to `/api/todos` returns data
- [ ] Database tab shows 6 default todos
- [ ] You can create a new todo
- [ ] Reset button works
- [ ] Postman collection downloads

If all checked, **you're live!** 🎉

---

**Remember:** Render's free tier sleeps after 15 minutes of inactivity. This is normal! The first request after sleep takes ~30 seconds to wake up. Just bookmark your URL and visit periodically to keep it warm.

**Happy Deploying!** 🚀
