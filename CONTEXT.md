# API Lab - AI Context Document

> This file helps AI coding assistants quickly understand the project structure, architecture, and recent changes.

---

## Project Overview

**API Lab** is an interactive learning platform that teaches APIs to non-technical users (BAs, PMs, QA testers) through hands-on experimentation in a browser-based sandbox.

**Key Philosophy:** Learning by doing, not reading. No terminal, no coding—just clicking and experimenting.

---

## Architecture at a Glance

### Tech Stack
- **Backend:** Flask 3.0 (Python)
- **Database:** SQLite (zero-config, auto-seeded)
- **Frontend:** Alpine.js (reactive) + Tailwind CSS (styling)
- **Auth:** Flask-JWT-Extended (JWT tokens) + Flask-HTTPAuth (Basic Auth)
- **Deployment:** Render (free tier) / Railway

### Core Components

```
Flask App (app.py)
  ├── Models (SQLAlchemy)
  │   ├── User (email, password_hash, role)
  │   ├── Todo (title, description, completed, owner_id)
  │   └── RequestLog (method, path, status_code, latency_ms)
  │
  ├── Routes (Blueprints)
  │   ├── /api/auth (login, token generation)
  │   ├── /api/todos (CRUD operations)
  │   ├── /api/admin (users, logs, DB tables, reset)
  │   ├── /api/scenarios (NEW - real-world workflow guides)
  │   └── /api/postman (collection download)
  │
  ├── Middleware
  │   ├── auth_middleware.py (Basic Auth + JWT)
  │   ├── logging_middleware.py (Request logging)
  │   └── error_playground.py (NEW - simulates API failures)
  │
  └── Frontend (Alpine.js SPA)
      ├── Playground Tab (API request builder)
      ├── Scenarios Tab (NEW - step-by-step workflows)
      ├── Database Tab (live table viewer)
      ├── Logs Tab (request history)
      └── Settings Tab (reset DB, error playground toggle)
```

---

## Recent Major Changes (Phase 13-18)

### Feature 1: Real-World Scenarios (Completed)

**Purpose:** Teach multi-step API workflows by mapping the Todo API to real-world use cases.

**Files Added:**
- `app/utils/scenarios.py` - 4 pre-built scenarios with 18 total steps
- `app/routes/scenarios.py` - REST endpoints for scenarios

**Scenarios Implemented:**
1. **🛒 E-commerce Checkout** (5 steps) - Shopping cart → Checkout flow
2. **📱 Social Media Post** (5 steps) - Create → Edit → Delete post
3. **✈️ Flight Booking** (5 steps) - Search → Reserve → Confirm
4. **✅ Task Management** (4 steps) - Direct Todo API usage

**How It Works:**
- User selects a scenario from the Scenarios tab
- Each step shows:
  - HTTP method, endpoint, auth type
  - Educational explanation
  - Real-world mapping (e.g., "POST /api/todos maps to POST /api/cart/items")
  - Learning point (e.g., "POST creates resources, server assigns IDs")
- "Auto-Fill" button pre-populates the Playground tab
- User executes request, then moves to next step

**API Endpoints:**
- `GET /api/scenarios` - List all scenarios
- `GET /api/scenarios/{id}` - Get scenario details with steps

---

### Feature 2: Error Playground (Completed)

**Purpose:** Simulate realistic API failures to teach error handling.

**Files Added:**
- `app/middleware/error_playground.py` - Middleware that randomly injects errors

**How It Works:**
- User enables Error Playground in Settings tab
- Sets chaos level (5%-50% failure rate) and optional latency
- When enabled, query params appended: `?error_playground=true&chaos_level=0.1&simulate_latency=500`
- Middleware randomly fails requests with educational error messages

**Simulated Errors:**
- 408 Request Timeout
- 429 Too Many Requests (Rate Limit)
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable

**Error Response Format:**
```json
{
  "code": "SIMULATED_RATE_LIMIT",
  "error": "Too Many Requests - You've exceeded the rate limit",
  "explanation": "APIs limit request frequency. Implement rate limiting on client side or upgrade your plan.",
  "hint": "🔥 This is a simulated error from Error Playground. Turn it off in Settings."
}
```

---

## Frontend Architecture (Alpine.js)

### State Management
All state lives in `appData()` function in `index.html`:

```javascript
{
  // Tab & UI state
  activeTab: 'playground',
  activeLesson: 'api',
  
  // Request state
  method: 'GET',
  endpoint: '/api/todos',
  authType: 'none',
  token: null,
  requestBody: '...',
  response: null,
  
  // Scenarios state (NEW)
  scenarios: [],
  currentScenario: null,
  currentStep: 0,
  
  // Error Playground state (NEW)
  errorPlaygroundEnabled: false,
  chaosLevel: 0.1,
  simulateLatency: 0,
  
  // Database state
  dbData: { todos: [], users: [], request_logs: [] }
}
```

### Key Functions
- `sendRequest()` - Makes API calls, appends error playground params if enabled
- `login()` - Gets JWT token from `/api/auth/login`
- `loadScenarios()` - Fetches scenario list
- `loadScenarioDetails(id)` - Loads specific scenario
- `prefillFromScenario()` - Auto-fills Playground from scenario step
- `loadDatabaseTables()` - Fetches DB table data
- `resetDatabase()` - Calls `/api/admin/reset`

---

## Database Schema

### Users Table
```sql
id          INTEGER PRIMARY KEY
email       TEXT UNIQUE NOT NULL
password_hash TEXT NOT NULL
role        TEXT DEFAULT 'user'  -- 'user' or 'admin'
created_at  TIMESTAMP
```

### Todos Table
```sql
id          INTEGER PRIMARY KEY
title       TEXT NOT NULL
description TEXT
completed   BOOLEAN DEFAULT FALSE
owner_id    INTEGER FOREIGN KEY → users.id
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

### Request_Logs Table
```sql
id          INTEGER PRIMARY KEY
method      TEXT
path        TEXT
status_code INTEGER
latency_ms  INTEGER
auth_method TEXT  -- 'none', 'basic', 'token'
timestamp   TIMESTAMP
```

---

## Authentication Flow

### Basic Auth
1. User provides email + password in Playground
2. Frontend encodes as `base64(email:password)`
3. Sends `Authorization: Basic <encoded_credentials>`
4. Backend decodes and verifies every request

### Token Auth (JWT)
1. User calls `POST /api/auth/login` with email + password
2. Server verifies credentials, generates JWT (24h expiry)
3. Frontend stores token in `localStorage`
4. Subsequent requests send `Authorization: Bearer <token>`
5. Middleware validates token signature and expiry

---

## Deployment Notes

### Port Configuration
- Default port: 5000 (conflicts with macOS AirPlay)
- Override with: `PORT=5001 python app.py`
- Render/Railway auto-assign PORT environment variable

### Database Initialization
- Database auto-seeds on first run if empty
- Seed data: 2 users (admin, testuser) + 6 sample todos
- Reset endpoint clears all data and re-seeds

### Free Tier Limitations
- **Render:** App sleeps after 15 min inactivity, first request takes ~30s to wake
- **Railway:** $5 free credit/month, no auto-sleep

---

## Common Development Tasks

### Add a New Scenario
1. Edit `app/utils/scenarios.py`
2. Add new scenario dict to `SCENARIOS` list
3. Follow existing structure (id, name, description, steps)
4. No code changes needed—scenarios are data-driven

### Add a New Error Type
1. Edit `app/middleware/error_playground.py`
2. Add new error dict to `ERROR_TYPES` list
3. Include code, message, explanation

### Modify UI
1. All UI is in `app/static/index.html`
2. HTML uses Alpine.js directives (`x-show`, `x-model`, `@click`)
3. Tailwind CSS classes for styling
4. No build step—just refresh browser

### Add New API Endpoint
1. Create route file in `app/routes/`
2. Register blueprint in `app/__init__.py`
3. Follow existing patterns for auth (`@jwt_required()` or `@auth.login_required`)

---

## Testing Credentials

**Regular User:**
- Email: `testuser@apilab.dev`
- Password: `test123`
- Can: CRUD own todos, view own data

**Admin User:**
- Email: `admin@apilab.dev`
- Password: `admin123`
- Can: View all users, logs, DB tables, reset database

---

## File Reference

### Critical Files (Modify with Care)
- `app/__init__.py` - App factory, registers blueprints/middleware
- `app/static/index.html` - Entire frontend UI
- `app/models/*.py` - Database schema (migrations not automated)

### Data Files (Safe to Edit)
- `app/utils/scenarios.py` - Scenario definitions
- `app/middleware/error_playground.py` - Error simulation logic

### Config Files
- `requirements.txt` - Python dependencies
- `render.yaml` - Render deployment config
- `railway.json` - Railway deployment config

---

## Known Issues & Quirks

### Port 5000 Conflict
- macOS AirPlay Receiver uses port 5000 by default
- **Solution:** Run with `PORT=5001 python app.py`

### Database Reset
- Reset only affects current instance
- On Render free tier, database resets when dyno restarts
- This is intentional—it's a learning sandbox, not production

### Token Expiry
- JWT tokens expire after 24 hours
- Frontend doesn't auto-refresh tokens
- User must re-login if token expires

### Error Playground Query Params
- Parameters persist in URL if navigating back
- Not an issue—middleware checks `error_playground=true` flag

---

## Next Steps / Roadmap

### Short-Term Enhancements
1. **Scenario Progress Tracking** - Save which steps user completed
2. **Custom Scenarios** - UI to let users create their own workflows
3. **Error Playground Stats** - Show count of simulated errors
4. **Export Scenario as Postman** - Generate collection from scenario

### Medium-Term Features
1. **OAuth2 Auth** - Add OAuth flow scenario
2. **Webhook Simulator** - Teach webhook concepts
3. **GraphQL Endpoint** - Compare REST vs GraphQL
4. **Rate Limiting** - Add actual rate limiting to teach the concept

### Long-Term Ideas
1. **Multi-user Collaboration** - Share scenarios with others
2. **Leaderboard** - Gamify learning with points
3. **Video Tutorials** - Embedded walkthrough videos
4. **Jupyter Notebook Integration** - Python client examples

---

## AI Assistant Tips

When working on this codebase:

1. **Frontend Changes:** Only modify `app/static/index.html` (single-file SPA)
2. **Backend Changes:** Add routes in `app/routes/`, register in `app/__init__.py`
3. **New Scenarios:** Edit `app/utils/scenarios.py` (data-driven, no code changes)
4. **Testing:** Run `PORT=5001 python app.py`, test at `http://localhost:5001`
5. **Error Handling:** All errors return JSON with `error` key
6. **Auth:** Protected routes need `@jwt_required()` or `@auth.login_required`
7. **Database:** Use `db.session` for queries, `db.session.commit()` to save

---

## Example Workflow: Adding a New Scenario

```python
# 1. Edit app/utils/scenarios.py

SCENARIOS.append({
    "id": "payment-processing",
    "name": "💳 Payment Processing",
    "description": "Learn how payment APIs handle transactions",
    "difficulty": "Intermediate",
    "duration": "8 minutes",
    "learning_goals": [
        "Understand idempotency in payment APIs",
        "Learn about transaction states",
        "Handle payment failures gracefully"
    ],
    "steps": [
        {
            "number": 1,
            "title": "Create Payment Intent",
            "method": "POST",
            "endpoint": "/api/todos",
            "auth_type": "token",
            "body": {
                "title": "Payment Intent: $50.00",
                "description": "User: John Doe, Card: **** 4242",
                "completed": False
            },
            "explanation": "In Stripe/PayPal, this is POST /api/payment_intents. The todo represents a pending payment.",
            "learning_point": "Payment intents are created BEFORE charging the card. This allows 3D Secure checks.",
            "real_world_mapping": "POST /api/payment_intents → {amount: 5000, currency: 'usd'}",
            "expected_result": "Payment intent created with ID"
        },
        # ... more steps
    ]
})
```

```bash
# 2. Restart server
PORT=5001 python app.py

# 3. Test endpoint
curl http://localhost:5001/api/scenarios/payment-processing | python -m json.tool

# 4. Verify in UI
# Open http://localhost:5001 → Scenarios tab → See new scenario
```

---

## Questions to Ask When Modifying

- **Adding a route:** Does it need auth? Use `@jwt_required()` or `@auth.login_required`
- **Changing DB schema:** Did you update the model AND the seed data?
- **Adding UI:** Did you add Alpine.js state in `appData()`?
- **New error type:** Does it have an educational explanation?
- **Breaking change:** Will this affect existing Postman collections?

---

**Last Updated:** 2026-02-13 (Phase 13-18 - Scenarios + Error Playground)
