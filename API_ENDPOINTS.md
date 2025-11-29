# VeganAI Coach API Endpoints

## Base URL
- Local: `http://localhost:8000`
- Docker: `http://localhost:8080` (or your mapped port)

## Interactive API Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## User Endpoints

### Create/Get User
```bash
POST /api/users
```

**Response:**
```json
{
  "id": 1,
  "created_at": "2025-11-29T08:00:00",
  "preferences_json": {}
}
```

### Get User by ID
```bash
GET /api/users/{user_id}
```

---

## Goal Endpoints

### Create Goal
```bash
POST /api/goals
Content-Type: application/json

{
  "title": "Learn dough types",
  "description": "Master different types of vegan dough",
  "target_recipes_per_week": 2,
  "target_skill": "dough types"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "Learn dough types",
  "description": "Master different types of vegan dough",
  "target_recipes_per_week": 2,
  "target_skill": "dough types",
  "status": "active",
  "created_at": "2025-11-29T08:00:00",
  "updated_at": null
}
```

### List Goals
```bash
GET /api/goals?status=active
```

**Query Parameters:**
- `status` (optional): Filter by status (`active`, `completed`, `paused`)

### Get Goal by ID
```bash
GET /api/goals/{goal_id}
```

### Update Goal
```bash
PUT /api/goals/{goal_id}
Content-Type: application/json

{
  "title": "Updated title",
  "status": "completed"
}
```

### Delete Goal
```bash
DELETE /api/goals/{goal_id}
```

---

## Recipe Q&A (Existing)

### Ask Chef
```bash
POST /ask
Content-Type: application/json

{
  "question": "How do I make vegan pizza dough?"
}
```

---

## Testing with cURL

### Create a Goal
```bash
curl -X POST "http://localhost:8000/api/goals" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn dough types",
    "description": "Master different types of vegan dough",
    "target_recipes_per_week": 2,
    "target_skill": "dough types"
  }'
```

### List Goals
```bash
curl "http://localhost:8000/api/goals"
```

### Get Goal
```bash
curl "http://localhost:8000/api/goals/1"
```

---

## Testing with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Create a goal
response = requests.post(f"{BASE_URL}/api/goals", json={
    "title": "Learn dough types",
    "description": "Master different types of vegan dough",
    "target_recipes_per_week": 2,
    "target_skill": "dough types"
})
print(response.json())

# List goals
response = requests.get(f"{BASE_URL}/api/goals")
print(response.json())
```

---

## Docker Testing

1. **Build image:**
   ```bash
   docker build -t veganai-coach .
   ```

2. **Run container:**
   ```bash
   docker run -p 8080:8080 \
     -e DATABASE_URL=sqlite:///./veganai.db \
     -e OPENAI_API_KEY=your_key \
     veganai-coach
   ```

3. **Test endpoints:**
   ```bash
   curl http://localhost:8080/api/goals
   ```

---

## Notes

- For MVP, `user_id` defaults to `1` in all endpoints
- In production, you'll get `user_id` from authentication
- Database migrations run automatically on Docker startup
- SQLite database file persists in container (consider using volumes for production)

