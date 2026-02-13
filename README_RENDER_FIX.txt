██████╗ ███████╗███╗   ██╗██████╗ ███████╗██████╗     ███████╗██╗██╗  ██╗
██╔══██╗██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██╔════╝██║╚██╗██╔╝
██████╔╝█████╗  ██╔██╗ ██║██║  ██║█████╗  ██████╔╝    █████╗  ██║ ╚███╔╝ 
██╔══██╗██╔══╝  ██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    ██╔══╝  ██║ ██╔██╗ 
██║  ██║███████╗██║ ╚████║██████╔╝███████╗██║  ██║    ██║     ██║██╔╝ ██╗
╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝╚═╝  ╚═╝

PROBLEM: Render keeps running "gunicorn app:app" instead of "gunicorn wsgi:app"

WHY: Render dashboard caches the start command. Your render.yaml is correct,
     but the dashboard setting OVERRIDES it!

═════════════════════════════════════════════════════════════════════════

DO THIS IN RENDER DASHBOARD (takes 1 minute):
═════════════════════════════════════════════════════════════════════════

1. Open Render Dashboard: https://dashboard.render.com

2. Click your service (probably called "apilab")

3. Left sidebar → Click "Settings"

4. Find "Start Command" field

5. It currently shows:
   gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1

6. Change to:
   gunicorn wsgi:app --bind 0.0.0.0:$PORT --timeout 120 --workers 1
   
   (Only change app:app → wsgi:app)

7. Click "Save Changes" button

8. Scroll up, click "Manual Deploy" tab

9. Click "Clear build cache & deploy"

10. Wait 2-3 minutes

═════════════════════════════════════════════════════════════════════════
✅ DEPLOYMENT WILL NOW SUCCEED!
═════════════════════════════════════════════════════════════════════════

Then commit your local changes:
  git add .
  git commit -m "fix: update wsgi.py for deployment"
  git push origin main

═════════════════════════════════════════════════════════════════════════

WHAT SUCCESS LOOKS LIKE IN LOGS:

==> Running 'gunicorn wsgi:app'              ← Should say "wsgi:app" not "app:app"
[INFO] Starting gunicorn 21.2.0
[INFO] Listening at: http://0.0.0.0:10000
[INFO] Booting worker with pid: 45
✅ Created instance directory
⚠️  Database is empty. Auto-seeding...
✅ Database seeded successfully!

═════════════════════════════════════════════════════════════════════════

THAT'S IT! Your app will be live at your Render URL.
