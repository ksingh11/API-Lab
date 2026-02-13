# 🚨 URGENT: Fix Start Command in Render Dashboard

## The Problem

Render is using a **cached start command** that still says `gunicorn app:app` even though we updated the code to `gunicorn wsgi:app`.

The error log shows:
```
==> Running 'gunicorn app:app'  ← This is WRONG!
```

It should be:
```
==> Running 'gunicorn wsgi:app'  ← This is CORRECT!
```

---

## ✅ SOLUTION (Do This NOW in Render Dashboard)

### Step 1: Go to Render Dashboard
1. Open https://dashboard.render.com
2. Click on your **apilab** service

### Step 2: Update Start Command
1. Click **"Settings"** in the left sidebar
2. Scroll down to **"Start Command"**
3. You'll see: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1`
4. **CHANGE IT TO:**
   ```
   gunicorn wsgi:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1
   ```
5. Click **"Save Changes"**

### Step 3: Manually Deploy
1. Go to **"Manual Deploy"** section
2. Select **"Clear build cache & deploy"**
3. Click **"Deploy"**

### Step 4: Watch Logs
After deploying, you should see:
```
==> Running 'gunicorn wsgi:app'  ← CORRECT!
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
✅ Created instance directory
✅ Database seeded successfully!
```

---

## Alternative Fix (If Settings Don't Stick)

If Render keeps reverting to `app:app`, try this:

### Option A: Delete and Recreate Service
1. Delete the current service in Render
2. Create a new web service
3. Connect your GitHub repo
4. Render will read `render.yaml` and use the correct command

### Option B: Use Environment Variable Override
1. In Render dashboard, go to **Environment**
2. Add a new environment variable:
   - **Key:** `GUNICORN_CMD_ARGS`
   - **Value:** (leave empty)
3. Then in **Settings** → **Start Command**, use:
   ```
   gunicorn wsgi:app
   ```
4. Render will add the `--bind` and other args automatically

---

## Why This Happened

When you first created the Render service, it read the start command from your initial push. Even though we updated `render.yaml`, Render's dashboard **overrides** the YAML file if a manual start command was set.

**Solution:** Always update the dashboard settings after changing `render.yaml`.

---

## Verification After Fix

After deployment succeeds, test:

1. **Visit your Render URL** (e.g., `https://apilab-xyz.onrender.com`)
2. **You should see the API Lab dashboard**
3. **Test login:**
   - Email: `testuser@apilab.dev`
   - Password: `test123`
4. **Make a test API request** to `/api/todos`
5. **Check Database tab** - should show 6 todos

If all of these work, **deployment is successful!** ✅

---

## Quick Checklist

- [ ] Changed start command in Render dashboard to `gunicorn wsgi:app`
- [ ] Saved changes
- [ ] Triggered manual deploy with cache clear
- [ ] Watched logs - saw `Running 'gunicorn wsgi:app'`
- [ ] Deployment succeeded
- [ ] Homepage loads
- [ ] Login works
- [ ] API requests work

---

## Still Not Working?

If you still get errors after this, share the **full deployment logs** and I'll help debug further. But this should 100% fix the issue.

The key is: **Render dashboard settings override render.yaml**, so you MUST update the dashboard!
