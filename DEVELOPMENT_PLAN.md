# VeganAI Coach - Development Plan

## Current State Analysis

### What You Have ✅
- **Backend**: FastAPI API with RAG system (ChromaDB + OpenAI)
- **Vector Database**: ChromaDB for recipe knowledge storage
- **Ingestion**: Basic text file loader for recipes
- **Q&A Endpoint**: `/ask` endpoint that answers questions using retrieved context
- **Docker**: Containerization setup ready

### What's Missing ❌
- User management and session handling
- Goal/path tracking system
- Recipe suggestion engine
- Feedback collection system
- Learning/adaptation system
- Recipe generation (not just retrieval)
- Image upload/processing
- Mobile-friendly frontend
- User preferences storage
- External content scraping (Instagram/web)

---

## Step-by-Step Development Plan

### **Phase 1: Foundation & Data Models** 🏗️

#### Step 1.1: Database Schema Design
**Goal**: Create persistent storage for users, goals, recipes, and feedback

**What to build:**
- SQLite or PostgreSQL database with tables:
  - `users` (id, created_at, preferences_json)
  - `goals` (id, user_id, title, description, target_recipes_per_week, target_skill, created_at, status)
  - `paths` (id, goal_id, name, description, steps)
  - `recipes` (id, title, ingredients, instructions, created_by_ai, source_url, metadata_json)
  - `recipe_suggestions` (id, user_id, goal_id, recipe_id, suggested_at, status)
  - `recipe_feedback` (id, recipe_id, user_id, liked, rating, changes_suggested, photo_path, ingredients_detected, feedback_text, created_at)
  - `user_preferences` (id, user_id, preference_type, preference_value, learned_from_feedback)

**Files to create:**
- `app/database.py` - Database connection and models (SQLAlchemy)
- `app/models.py` - Pydantic models for API requests/responses
- `app/migrations/` - Database migration scripts

---

### **Phase 2: Core User Features** 👤

#### Step 2.1: User & Goal Management
**Goal**: Allow users to set goals and learning paths

**Endpoints to create:**
- `POST /api/users` - Create/get user (or use session-based)
- `POST /api/goals` - Create a new learning goal
- `GET /api/goals/{goal_id}` - Get goal details
- `PUT /api/goals/{goal_id}` - Update goal
- `GET /api/goals` - List user's goals

**What to modify:**
- `app/main.py` - Add new endpoints
- Create `app/services/goal_service.py` - Business logic for goals

---

#### Step 2.2: Recipe Suggestion Engine
**Goal**: Suggest recipes based on goals and user context

**Endpoints to create:**
- `POST /api/recipes/suggest` - Get recipe suggestion based on goal
- `GET /api/recipes/{recipe_id}` - Get full recipe details

**Logic flow:**
1. User requests recipe suggestion
2. System checks active goals and progress
3. Retrieves relevant recipes from vector DB (RAG)
4. Filters/ranks based on goal criteria (e.g., "dough recipes")
5. Returns suggestion with explanation

**What to modify:**
- `app/main.py` - Add suggestion endpoint
- Create `app/services/recipe_service.py` - Recipe suggestion logic
- Enhance RAG chain to consider goals in prompt

---

### **Phase 3: Feedback & Learning System** 🧠

#### Step 3.1: Feedback Collection
**Goal**: Collect structured feedback after cooking

**Endpoints to create:**
- `POST /api/recipes/{recipe_id}/feedback` - Submit feedback
  - Body: `{liked: bool, rating: int, changes: str, photo: file, ingredients_detected: list}`
- `GET /api/recipes/{recipe_id}/feedback` - Get feedback history

**Features:**
- Image upload handling (store in `data/photos/`)
- Optional: Image analysis for ingredient detection (Vision API)
- Store feedback in database

**What to modify:**
- `app/main.py` - Add feedback endpoint with file upload
- Create `app/services/feedback_service.py`
- Add `python-multipart` to requirements.txt for file uploads

---

#### Step 3.2: Learning & Adaptation System
**Goal**: AI learns from feedback and adjusts future recipes

**Logic flow:**
1. When feedback is submitted, extract insights:
   - "too liquid" → learn about liquid ratios
   - "too spicy" → learn spice preferences
   - "loved the texture" → reinforce technique
2. Store learnings in `user_preferences` table
3. When suggesting next recipe, inject learnings into prompt:
   - "User prefers thicker curries (learned from feedback on recipe X)"
   - "User likes less salt (learned from 3 previous recipes)"

**What to create:**
- `app/services/learning_service.py` - Extract insights from feedback using LLM
- `app/services/preference_service.py` - Manage user preferences
- Enhance recipe suggestion to use preferences

**Example prompt enhancement:**
```
Based on user's feedback history:
- Recipe #1: "Curry was too liquid" → User prefers thicker curries
- Recipe #2: "Needed more salt" → User likes more seasoning
- Recipe #3: "Perfect texture" → User enjoyed the dough technique

When suggesting next recipe, consider these preferences.
```

---

### **Phase 4: Recipe Generation** 🎨

#### Step 4.1: AI Recipe Generation
**Goal**: Generate original recipes based on preferences and goals

**Endpoints to create:**
- `POST /api/recipes/generate` - Generate new recipe
  - Body: `{goal_id, user_comment, preferences_to_consider: bool}`

**Logic:**
1. Retrieve user's goal and preferences
2. Use LLM to generate recipe (not just retrieve)
3. Store generated recipe in database
4. Return recipe with explanation of why it was generated

**What to create:**
- `app/services/generation_service.py` - Recipe generation logic
- Enhanced prompt that combines:
  - Goal context ("learning dough types")
  - User preferences ("prefers thicker textures")
  - Base knowledge from vector DB (retrieved similar recipes)
  - Generation instructions

**Example prompt:**
```
You are creating a new vegan recipe for a user learning about dough types.
User's goal: Learn 2 recipes per week to master different dough types
User preferences: Prefers thicker textures, likes whole wheat flour
Context from similar recipes: [retrieved recipes]

Generate an original recipe that:
1. Teaches a new dough technique
2. Respects user preferences
3. Is achievable for their skill level
```

---

#### Step 4.2: External Content Integration
**Goal**: Scrape/ingest recipes from Instagram accounts or web pages

**Endpoints to create:**
- `POST /api/sources/add` - Add Instagram account or URL to follow
- `POST /api/sources/ingest` - Manually trigger ingestion from sources

**What to create:**
- `app/services/scraper_service.py` - Web scraping logic
  - Instagram: Use Instagram Basic Display API or scraping (with rate limits)
  - Web pages: Use BeautifulSoup/Playwright
- `app/services/source_service.py` - Manage recipe sources
- `app/ingest.py` - Enhance to support multiple sources

**Dependencies to add:**
- `beautifulsoup4` - Web scraping
- `requests` - HTTP requests
- `instaloader` or `instagram-scraper` - Instagram (optional, may need API)

---

### **Phase 5: Mobile Interface** 📱

#### Step 5.1: RESTful API Completion
**Goal**: Ensure all endpoints are mobile-friendly (JSON responses)

**What to verify:**
- All endpoints return proper JSON
- Error handling with clear messages
- CORS enabled for mobile apps
- Authentication/session handling (if needed)

**What to modify:**
- `app/main.py` - Add CORS middleware
- Ensure consistent response format

---

#### Step 5.2: Frontend Options
**Options:**
1. **Progressive Web App (PWA)** - HTML/JS that works on mobile
2. **React Native / Flutter** - Native mobile app
3. **Simple HTML Frontend** - For MVP, can use on mobile browser

**For MVP, recommend:**
- Simple HTML/JS frontend in `frontend/` directory
- Responsive design (mobile-first)
- Can be served by FastAPI or separate static server

**What to create:**
- `frontend/index.html` - Main app page
- `frontend/js/app.js` - Frontend logic
- `frontend/css/styles.css` - Mobile-responsive styles

---

### **Phase 6: Enhancement & Polish** ✨

#### Step 6.1: Advanced Features
- Recipe difficulty estimation
- Ingredient substitution suggestions
- Shopping list generation
- Progress tracking dashboard
- Recipe sharing between users

#### Step 6.2: Performance & Scalability
- Caching for frequent queries
- Background jobs for scraping
- Database indexing
- Vector DB optimization

---

## Recommended Next Steps (Priority Order)

### **Immediate (Week 1-2):**
1. ✅ **Add database layer** - SQLite with SQLAlchemy for persistence
2. ✅ **Create goal management endpoints** - Basic CRUD for goals
3. ✅ **Enhance recipe suggestion** - Use goals in RAG prompt

### **Short-term (Week 3-4):**
4. ✅ **Feedback collection endpoint** - Store feedback in database
5. ✅ **Basic learning system** - Extract preferences from feedback text
6. ✅ **Recipe generation** - LLM generates recipes (not just retrieves)

### **Medium-term (Week 5-6):**
7. ✅ **Image upload & processing** - Store photos, optional Vision API
8. ✅ **Mobile-friendly frontend** - Simple HTML/JS interface
9. ✅ **External source ingestion** - Web scraping for recipes

### **Long-term (Week 7+):**
10. ✅ **Advanced learning** - More sophisticated preference extraction
11. ✅ **Instagram integration** - If API access available
12. ✅ **Polish & optimization** - Performance, UX improvements

---

## Technical Decisions to Make

### Database Choice
- **SQLite** (recommended for MVP) - Simple, file-based, no setup
- **PostgreSQL** (for production) - Better for concurrent users

### Authentication
- **Session-based** (simple) - Store user_id in session
- **JWT tokens** (better for mobile) - Stateless authentication

### Image Storage
- **Local filesystem** (MVP) - Store in `data/photos/`
- **Cloud storage** (production) - S3, Cloudinary, etc.

### Frontend Framework
- **Vanilla JS** (fastest MVP) - Simple HTML/JS
- **React/Vue** (better UX) - More interactive
- **React Native** (native app) - Best mobile experience

---

## Files Structure (Proposed)

```
VeganAI-Coach/
├── app/
│   ├── main.py              # FastAPI app (enhance)
│   ├── database.py          # NEW: DB connection
│   ├── models.py            # NEW: Pydantic models
│   ├── db_models.py         # NEW: SQLAlchemy models
│   ├── services/
│   │   ├── goal_service.py      # NEW
│   │   ├── recipe_service.py     # NEW
│   │   ├── feedback_service.py   # NEW
│   │   ├── learning_service.py   # NEW
│   │   ├── generation_service.py # NEW
│   │   └── scraper_service.py    # NEW
│   ├── ingest.py            # Enhance for multiple sources
│   └── ask.py               # Keep for CLI
├── data/
│   ├── photos/              # NEW: User-uploaded photos
│   └── recipes/             # NEW: Scraped recipes
├── frontend/                # NEW: Web interface
│   ├── index.html
│   ├── js/
│   └── css/
├── migrations/              # NEW: DB migrations
└── requirements.txt         # Update with new deps
```

---

## What I Would Modify/Improve Next

### **1. Database Layer (Highest Priority)**
**Why**: Everything depends on persistent storage for users, goals, and feedback.

**Changes:**
- Add SQLAlchemy for ORM
- Create database models
- Add migration system (Alembic)
- Update `requirements.txt` with `sqlalchemy`, `alembic`

### **2. Goal Management System**
**Why**: Core feature - users need to set goals before getting suggestions.

**Changes:**
- Add `/api/goals` endpoints
- Create goal service
- Store goals in database
- Link goals to recipe suggestions

### **3. Enhanced Recipe Suggestion**
**Why**: Current system just answers questions. Need goal-aware suggestions.

**Changes:**
- Modify RAG chain to accept goal context
- Create recipe suggestion service
- Filter/rank recipes based on goal criteria
- Return structured recipe data (not just text)

### **4. Feedback Collection**
**Why**: Essential for learning system to work.

**Changes:**
- Add file upload endpoint
- Store feedback in database
- Basic image storage
- Optional: Vision API for ingredient detection

### **5. Learning System**
**Why**: The "magic" feature that makes it adaptive.

**Changes:**
- Create learning service that uses LLM to extract insights
- Store preferences in database
- Inject preferences into future recipe prompts
- Track what works and what doesn't

---

## Questions to Consider

1. **User Management**: Single-user app or multi-user? (affects database design)
2. **Authentication**: Needed for MVP or can start with session-based?
3. **Image Processing**: Use OpenAI Vision API for ingredient detection? (adds cost)
4. **Scraping**: Instagram API access or use scraping tools? (legal/rate limit concerns)
5. **Deployment**: Keep Docker setup? Deploy to cloud? (affects file storage strategy)

---

This plan provides a clear roadmap from your current RAG-based Q&A system to a full-featured adaptive recipe learning app. Start with Phase 1 (database) and work through sequentially.

