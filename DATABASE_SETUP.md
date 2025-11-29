# Database Setup Guide

## Overview

The VeganAI Coach uses SQLAlchemy with support for both **SQLite** (local development) and **PostgreSQL** (AWS RDS production).

## Database Models

The database consists of 7 main tables:

1. **users** - User accounts and general preferences
2. **goals** - Learning goals (e.g., "Learn 2 recipes per week to master dough types")
3. **paths** - Learning paths/steps within goals
4. **recipes** - Recipe storage (both AI-generated and scraped)
5. **recipe_suggestions** - Tracks recipe suggestions made to users
6. **recipe_feedback** - User feedback after cooking (likes, ratings, photos, changes)
7. **user_preferences** - Learned preferences extracted from feedback

## Configuration

### Local Development (SQLite)

By default, the app uses SQLite for local development. The database file will be created at `./veganai.db`.

No configuration needed - just run migrations!

### AWS Production (PostgreSQL)

For AWS deployment, set the `DATABASE_URL` environment variable:

```bash
export DATABASE_URL="postgresql://username:password@your-rds-endpoint:5432/veganai_db"
```

Or in your `.env` file:
```
DATABASE_URL=postgresql://username:password@your-rds-endpoint:5432/veganai_db
```

## Running Migrations

### Initialize Database (First Time)

```bash
python -m app.init_db
```

This will:
- Run all pending migrations
- Create all tables
- Set up the database schema

### Manual Migration Commands

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# See migration history
alembic history

# See current version
alembic current
```

## Using the Database in Code

### Get Database Session

```python
from app.database import get_db
from fastapi import Depends

@app.get("/example")
def example_endpoint(db: Session = Depends(get_db)):
    # Use db session here
    users = db.query(User).all()
    return users
```

### Create Records

```python
from app.db_models import User, Goal

# Create a user
user = User(preferences_json={})
db.add(user)
db.commit()
db.refresh(user)

# Create a goal
goal = Goal(
    user_id=user.id,
    title="Learn dough types",
    target_recipes_per_week=2,
    target_skill="dough types"
)
db.add(goal)
db.commit()
```

### Query Records

```python
from app.db_models import Goal

# Get all active goals for a user
goals = db.query(Goal).filter(
    Goal.user_id == user_id,
    Goal.status == "active"
).all()

# Get a specific goal
goal = db.query(Goal).filter(Goal.id == goal_id).first()
```

## Database Schema Details

### Users Table
- `id` (Primary Key)
- `created_at` (Timestamp)
- `preferences_json` (JSON field for general preferences)

### Goals Table
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `title` (String, max 200 chars)
- `description` (Text)
- `target_recipes_per_week` (Integer)
- `target_skill` (String, max 100 chars)
- `status` (String: "active", "completed", "paused")
- `created_at`, `updated_at` (Timestamps)

### Recipes Table
- `id` (Primary Key)
- `title` (String, max 200 chars)
- `ingredients` (Text)
- `instructions` (Text)
- `created_by_ai` (Boolean)
- `source_url` (String, max 500 chars, nullable)
- `metadata_json` (JSON field)
- `created_at` (Timestamp)

### Recipe Feedback Table
- `id` (Primary Key)
- `recipe_id` (Foreign Key → recipes.id)
- `user_id` (Foreign Key → users.id)
- `liked` (Boolean, nullable)
- `rating` (Integer 1-5, nullable)
- `changes_suggested` (Text, nullable)
- `photo_path` (String, max 500 chars, nullable)
- `ingredients_detected` (JSON array, nullable)
- `feedback_text` (Text, nullable)
- `created_at` (Timestamp)

### User Preferences Table
- `id` (Primary Key)
- `user_id` (Foreign Key → users.id)
- `preference_type` (String, max 100 chars) - e.g., "texture", "spice_level"
- `preference_value` (Text) - e.g., "thicker", "less spicy"
- `learned_from_feedback` (Foreign Key → recipe_feedback.id, nullable)
- `confidence` (Float 0-1)
- `created_at` (Timestamp)

## AWS RDS Setup

When deploying to AWS:

1. **Create RDS PostgreSQL Instance**
   - Use PostgreSQL 13+ (recommended: 15)
   - Enable public access if needed (or use VPC)
   - Note the endpoint URL

2. **Set Environment Variable**
   ```bash
   DATABASE_URL=postgresql://username:password@your-endpoint.region.rds.amazonaws.com:5432/veganai_db
   ```

3. **Run Migrations**
   ```bash
   alembic upgrade head
   ```

4. **Connection Pooling**
   - The database.py already includes `pool_pre_ping=True` for RDS
   - Consider using RDS Proxy for production workloads

## Backup & Maintenance

### SQLite Backup
```bash
cp veganai.db veganai.db.backup
```

### PostgreSQL Backup (AWS)
```bash
pg_dump $DATABASE_URL > backup.sql
```

### Restore
```bash
psql $DATABASE_URL < backup.sql
```

## Troubleshooting

### Migration Errors
- Make sure all models are imported in `alembic/env.py`
- Check that `DATABASE_URL` is set correctly
- Verify database connection permissions

### Connection Issues (AWS)
- Check security group rules (allow port 5432)
- Verify VPC configuration
- Check RDS instance status

### SQLite Lock Errors
- SQLite doesn't handle concurrent writes well
- For production, use PostgreSQL
- For local dev, ensure only one process accesses the DB

