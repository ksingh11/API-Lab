# 🧪 API Lab - Interactive API Learning Sandbox

> Learn APIs by doing—no terminal, no coding, just clicking and experimenting.

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/yourusername/apilab)

---

## What is API Lab?

API Lab is a **flight simulator for APIs**. A safe playground where you can:

- ✅ Make real API requests from your browser
- ✅ See live database changes in real-time
- ✅ Learn HTTP, REST, JSON, and authentication
- ✅ Break things and reset instantly
- ✅ Export to Postman for professional testing
- ✅ Experience both Basic Auth and Token Auth
- ✅ Follow real-world scenario workflows (e-commerce, social media, etc.)
- ✅ Simulate API errors to learn error handling

**Perfect for:** Business Analysts, Project Managers, QA testers, students, or anyone curious about APIs.

---

## 🚀 Quick Start (Choose One)

### Option 1: Run Locally (One Command) ⚡

**Mac/Linux:**
```bash
git clone https://github.com/yourusername/apilab.git
cd apilab
./start.sh
```

**Windows:**
```batch
git clone https://github.com/yourusername/apilab.git
cd apilab
start.bat
```

Then open: **http://localhost:5000**

---

### Option 2: Deploy to Render (Free Hosting) ☁️

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

1. Click the button above
2. Sign up for Render (free tier, no credit card)
3. Connect your GitHub repository
4. Wait ~2 minutes for deployment
5. Click your app URL and start learning!

**⚠️ Note:** Render free tier sleeps after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

**📖 Detailed Deploy Guide:** See [DEPLOY.md](DEPLOY.md) for step-by-step instructions with screenshots.

---

### Option 3: Deploy to Railway (Alternative) 🚂

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/apilab)

1. Click the button above
2. Sign up for Railway (free $5 credit)
3. Database persists in a volume
4. No auto-sleep (faster response times)

---

## 📚 What You'll Learn

| Topic | Duration | Description |
|-------|----------|-------------|
| **API Basics** | 10 min | What is an API? What is REST? |
| **HTTP Methods** | 15 min | GET, POST, PUT, DELETE |
| **Status Codes** | 10 min | Understanding 200, 404, 500, etc. |
| **JSON** | 10 min | How APIs exchange data |
| **Authentication** | 20 min | Basic Auth vs Token Auth (JWT) |
| **Database Interaction** | 10 min | See how requests change data |
| **Real-World Scenarios** | 20 min | E-commerce, social media, booking workflows |
| **Error Handling** | 15 min | Learn to handle failures gracefully |

**Total: ~110 minutes to API literacy** 🎓

---

## ✨ Features

### 🚀 Visual API Playground
- **No curl needed:** Point-and-click request builder
- **Multiple auth methods:** Basic Auth + JWT Token
- **Real-time testing:** Send requests and see responses instantly
- **JSON editor:** Auto-format and validate JSON

### 📊 Live Database Viewer
- **Spreadsheet-style tables:** View todos, users, logs
- **Real-time updates:** Watch data change as you make requests
- **Auto-refresh:** Optional 5-second polling
- **Export options:** Download as CSV or JSON

### 📜 Request History
- **Flight recorder:** See all your API calls
- **Full details:** Method, path, status, latency, body
- **Replay requests:** Quickly test again
- **Filter & search:** Find specific requests

### 🔐 Dual Authentication
- **Basic Auth:** Send credentials with every request
- **Token Auth (JWT):** Login once, reuse token for 24 hours
- **Learn the difference:** See why modern APIs use tokens

### 📮 Postman Integration
- **Downloadable collection:** One-click export
- **All endpoints included:** Pre-configured requests
- **Test credentials:** Ready to use examples
- **Auto-save tokens:** Smart test scripts included

### 🔄 Reset Anytime
- **Big red button:** Restore to defaults instantly
- **No consequences:** Safe to experiment
- **Seed data:** 2 users + 5 todos restored

### 📖 Built-in Learning
- **Interactive sidebar:** Lessons on API concepts
- **Context-sensitive help:** Explanations for each status code
- **Glossary:** Hover definitions for technical terms
- **No external docs needed:** Everything in one place

### 📖 Real-World Scenarios (NEW!)
- **Step-by-step workflows:** Learn multi-step API patterns
- **4 pre-built scenarios:** E-commerce, social media, flight booking, task management
- **Auto-fill requests:** One-click to populate request details
- **Real-world mapping:** See how Todo API maps to actual use cases
- **Progress tracking:** Visual progress bar through each scenario

### 🔥 Error Playground (NEW!)
- **Simulated failures:** Random errors to teach error handling
- **Configurable chaos level:** 5%-50% failure rate
- **Educational explanations:** Learn what each error means
- **Realistic errors:** 408 Timeout, 429 Rate Limit, 500 Server Error, 503 Unavailable
- **Latency simulation:** Test timeout handling with artificial delays

---

## 🎯 First Steps

After opening API Lab:

1. **Try a scenario** - Click "Scenarios" tab and pick "E-commerce Checkout" for a guided tour
2. **Explore the playground** - Try making a GET request to `/api/todos`
3. **Login for a token** - Use `testuser@apilab.dev` / `test123`
4. **Create a todo** - Send a POST request and watch the database update
5. **View the database** - Click the "Database" tab to see your todo appear
6. **Enable Error Playground** - Go to Settings and turn on error simulation to practice error handling
7. **Download Postman collection** - Click the button in the header
8. **Reset when ready** - Hit the reset button to start over

**No programming knowledge needed!**

---

## 🔑 Test Credentials

### Regular User
```
Email:    testuser@apilab.dev
Password: test123
Role:     user
```

### Admin User (for admin endpoints)
```
Email:    admin@apilab.dev
Password: admin123
Role:     admin
```

---

## 📖 API Documentation

### Base URL
```
Local:      http://localhost:5000/api
Production: https://your-app.onrender.com/api
```

### Public Endpoints

#### Health Check
```http
GET /api/health

Response: 200 OK
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-02-13T10:30:00Z"
}
```

#### Login (Get JWT Token)
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "testuser@apilab.dev",
  "password": "test123"
}

Response: 200 OK
{
  "token": "eyJhbGc...",
  "user": {...},
  "expires_in": 86400
}
```

### Protected Endpoints (Require Auth)

#### List Todos
```http
GET /api/todos
Authorization: Basic dGVzdHVzZXI6dGVzdDEyMw==
  OR
Authorization: Bearer eyJhbGc...

Response: 200 OK
{
  "data": [
    {
      "id": 1,
      "title": "Learn what an API is",
      "completed": true,
      ...
    }
  ],
  "count": 5
}
```

#### Create Todo
```http
POST /api/todos
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "My new todo",
  "description": "Optional description",
  "completed": false
}

Response: 201 Created
{
  "data": {
    "id": 42,
    "title": "My new todo",
    ...
  }
}
```

#### Update Todo
```http
PUT /api/todos/{id}
Authorization: Bearer eyJhbGc...
Content-Type: application/json

{
  "title": "Updated title",
  "completed": true
}

Response: 200 OK
```

#### Delete Todo
```http
DELETE /api/todos/{id}
Authorization: Bearer eyJhbGc...

Response: 204 No Content
```

### Admin Endpoints (Admin Role Required)

#### Get All Users
```http
GET /api/admin/users
Authorization: Bearer eyJhbGc... (admin token)

Response: 200 OK
{
  "data": [...],
  "count": 2
}
```

#### Get Request Logs
```http
GET /api/admin/logs?limit=50
Authorization: Bearer eyJhbGc... (admin token)

Response: 200 OK
{
  "data": [...],
  "count": 23
}
```

#### View Database Tables
```http
GET /api/admin/db/tables/{table_name}
Authorization: Bearer eyJhbGc... (admin token)

table_name: todos | users | request_logs

Response: 200 OK
{
  "table": "todos",
  "rows": [...],
  "count": 5
}
```

#### Reset Database
```http
POST /api/admin/reset
Authorization: Bearer eyJhbGc... (admin token)

Response: 200 OK
{
  "message": "Database reset successfully",
  "seed_data": {
    "users": 2,
    "todos": 5
  }
}
```

#### Download Postman Collection
```http
GET /api/postman/collection

Response: 200 OK (JSON file download)
```

#### List All Scenarios
```http
GET /api/scenarios

Response: 200 OK
{
  "data": [
    {
      "id": "ecommerce-checkout",
      "name": "🛒 E-commerce Checkout Flow",
      "description": "Learn how shopping cart APIs work...",
      "difficulty": "Beginner",
      "duration": "5 minutes",
      "step_count": 5
    },
    ...
  ],
  "count": 4
}
```

#### Get Scenario Details
```http
GET /api/scenarios/{scenario_id}

Response: 200 OK
{
  "data": {
    "id": "ecommerce-checkout",
    "name": "🛒 E-commerce Checkout Flow",
    "steps": [
      {
        "number": 1,
        "title": "View Shopping Cart",
        "method": "GET",
        "endpoint": "/api/todos",
        "auth_type": "token",
        "explanation": "...",
        "learning_point": "...",
        "real_world_mapping": "..."
      },
      ...
    ]
  }
}
```

### Error Playground

Add these query parameters to any endpoint to simulate errors:

```http
GET /api/todos?error_playground=true&chaos_level=0.3&simulate_latency=1000
Authorization: Bearer eyJhbGc...

# With 30% chaos_level, ~3 out of 10 requests will fail randomly
# Possible errors: 408, 429, 500, 502, 503
# Each error includes educational explanations
```

---

## 🛠️ Tech Stack

| Component | Technology | Why? |
|-----------|------------|------|
| **Backend** | Flask 3.0 | Simple, explicit, teaching-friendly |
| **Database** | SQLite | Zero-config, portable |
| **Frontend** | Alpine.js + Tailwind | Reactive, no build step |
| **Auth** | Flask-JWT-Extended + HTTPAuth | Both Basic & Token auth |
| **Docs** | OpenAPI/Postman | Industry-standard formats |
| **Deploy** | Render/Railway | Free tier, persistent disk |

---

## 🤔 FAQ

### Q: Do I need to know how to code?
**A:** Nope! Everything is point-and-click. The UI guides you through each step.

### Q: Will this teach me programming?
**A:** No, but it'll help you understand how APIs work, which is useful for many non-coding roles (PM, BA, QA, etc.).

### Q: Can I break anything?
**A:** Yes! That's the point. Just hit "Reset" to restore defaults. It's a safe sandbox.

### Q: Is my data saved permanently?
**A:** Only in your browser/instance. This is for learning, not production use. On Render's free tier, data may reset when the server sleeps.

### Q: How much does it cost?
**A:** Zero. It's open source and deploys to free hosting tiers (Render, Railway).

### Q: Can I use this to learn Postman?
**A:** Absolutely! Click "Download Postman Collection" and import it into Postman. All requests are pre-configured.

### Q: What's the difference between Basic Auth and Token Auth?
**A:** 
- **Basic Auth:** You send your username/password with EVERY request. Simple but less secure.
- **Token Auth:** You login ONCE, get a token, and reuse it. The token expires after 24 hours. More secure and modern.

### Q: Why does my Render deployment sleep?
**A:** Render's free tier puts your app to sleep after 15 minutes of inactivity. The first request wakes it up (~30 seconds). This is normal! Just bookmark your URL and visit periodically to keep it warm.

### Q: Can I deploy to my own server?
**A:** Yes! You can run it anywhere Python is supported. Just follow the local setup steps and deploy the same way.

---

## 🏗️ Project Structure

```
apilab/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration
│   ├── models/                  # Database models (User, Todo, RequestLog)
│   ├── routes/                  # API endpoints (auth, todos, admin, postman, scenarios)
│   ├── middleware/              # Auth, logging, error playground middleware
│   ├── utils/                   # Helpers (seed, postman generator, scenarios)
│   └── static/
│       └── index.html           # Dashboard UI (Alpine.js)
├── instance/
│   └── apilab.db                # SQLite database (gitignored)
├── requirements.txt             # Python dependencies
├── render.yaml                  # Render deployment config
├── Procfile                     # Heroku-style process file
├── runtime.txt                  # Python version
├── railway.json                 # Railway deployment config
├── app.py                       # Entry point
├── seed.py                      # Database seeder
├── start.sh                     # Local setup script (Unix/Mac)
├── start.bat                    # Local setup script (Windows)
└── README.md                    # This file
```

---

## 🤝 Contributing

Found a bug? Have an idea? Want to add a feature?

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Ideas for contributions:**
- Additional scenarios (payment processing, user registration, file uploads)
- More auth methods (OAuth2, API keys)
- GraphQL endpoint
- Rate limiting examples
- Webhook simulator
- Dark mode toggle
- Mobile-responsive improvements
- Custom scenario builder (let users create their own workflows)
- Error playground statistics (track how many errors were simulated)

---

## 📜 License

MIT License - Free to use for learning or teaching, commercially or personally.

---

## 🙏 Acknowledgments

Built for people learning APIs. Inspired by the idea that **learning should feel like play, not work**.

Special thanks to:
- The Flask community for making Python web development simple
- Alpine.js for reactive UI without build complexity
- Tailwind CSS for rapid prototyping
- The API education community for feedback

---

## 📞 Support

- **Documentation:** See `API_LAB_SPEC.md` for detailed specifications
- **Issues:** [Open an issue](https://github.com/yourusername/apilab/issues)
- **Discussions:** [Join the discussion](https://github.com/yourusername/apilab/discussions)

---

**Made with ❤️ for people learning APIs**

*Remember: The best way to learn is by doing. Go ahead, break things!* 🚀
