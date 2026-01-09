# PostgreSQL in WSL (Ubuntu 24.04) — VisionGuard Step-by-Step

Use this if you’re running the backend inside WSL and you want the database to also run inside WSL.

Why this works: the backend connects to `localhost:5432` inside WSL, so networking is simple (no Windows firewall / pg_hba / listen_addresses issues).

---

## 0) Confirm where you’re running the backend

If your backend path looks like:

- `/home/.../backend-visionguard-ai/...`

you are running inside WSL. This guide assumes that.

---

## 1) Install PostgreSQL in WSL

In a WSL Ubuntu terminal:

```bash
sudo apt update
sudo apt install -y postgresql postgresql-contrib
```

---

## 2) Start the Postgres service

Depending on your WSL/systemd setup, one of these will work:

### Option A (systemd enabled in WSL)
```bash
sudo systemctl start postgresql
sudo systemctl status postgresql --no-pager
```

### Option B (service command)
```bash
sudo service postgresql start
sudo service postgresql status
```

You want to see it running.

---

## 3) Create the database + user for VisionGuard

### 3.1 Switch into the Postgres admin user

```bash
sudo -u postgres psql
```

### 3.2 Run these SQL commands

Replace `strong_password_here` with your own password.

```sql
-- Create DB
CREATE DATABASE visionguard_db;

-- Create dedicated user
CREATE USER visionguard_user WITH PASSWORD 'strong_password_here';

-- Give access
GRANT ALL PRIVILEGES ON DATABASE visionguard_db TO visionguard_user;

-- Make the user the DB owner (recommended, avoids permission issues)
ALTER DATABASE visionguard_db OWNER TO visionguard_user;

-- (Optional but recommended) allow the user to create schema objects in public
\c visionguard_db
ALTER SCHEMA public OWNER TO visionguard_user;
GRANT ALL ON SCHEMA public TO visionguard_user;
GRANT CREATE ON SCHEMA public TO visionguard_user;
```

Exit psql:

```sql
\q
```

---

## 4) Point the backend to the WSL Postgres (edit `.env`)

In `backend-visionguard-ai/`, create your runtime env file:

```bash
cd ~/visionguard-main/backend-visionguard-ai
cp .env.example .env
```

Edit `.env` and set:

```env
DATABASE_URL=postgresql://visionguard_user:strong_password_here@localhost:5432/visionguard_db
```

Notes:
- Use `localhost` (not `10.255...`), because Postgres is now inside WSL.
- Don’t edit `.env.example` for secrets; only edit `.env`.

---

## 5) Restart the backend

From `backend-visionguard-ai/`:

```bash
python main.py
```

On startup you should see:
- `✓ Database initialized successfully`

If you still see DB errors:
- confirm the Postgres service is running
- confirm your password is correct

---

## 6) Verify the DB connection (quick test)

Run:

```bash
psql "postgresql://visionguard_user:strong_password_here@localhost:5432/visionguard_db" -c "SELECT 1;"
```

If it prints `1`, the DB is reachable and credentials are correct.

---

## 7) Tables: how they get created

This backend creates tables automatically on startup using SQLAlchemy (`init_db()` → `Base.metadata.create_all`).

So once the DB connects, tables should appear under `visionguard_db`.

## If you get: `relation "users" does not exist`

That means the database connection works, but the tables were not created.

Do this from `backend-visionguard-ai/`:

1) Ensure you’re using the correct DB URL in `.env` (WSL Postgres should be `@localhost:5432`).
2) Run a one-time table creation command:

```bash
python -c "from app.db.base import init_db; init_db(); print('DB tables created (or already existed).')"
```

3) Verify tables exist:

```bash
sudo -u postgres psql -d visionguard_db -c "\\dt"
```

If step (2) fails with a permissions error (common if you created a user but didn’t grant schema rights), run:

```bash
sudo -u postgres psql -d visionguard_db -c "GRANT ALL ON SCHEMA public TO visionguard_user;"
```

Then re-run the one-time table creation command.

## If you get: `permission denied for schema public`

Example error:
- `psycopg2.errors.InsufficientPrivilege: permission denied for schema public`
- Often happens when SQLAlchemy tries to create tables or enum types (e.g. `CREATE TYPE userrole AS ENUM ...`).

Fix it by making your app user the owner of the DB + schema (run as the `postgres` OS user):

```bash
sudo -u postgres psql -c "ALTER DATABASE visionguard_db OWNER TO visionguard_user;"
sudo -u postgres psql -d visionguard_db -c "ALTER SCHEMA public OWNER TO visionguard_user;"
sudo -u postgres psql -d visionguard_db -c "GRANT ALL ON SCHEMA public TO visionguard_user;"
sudo -u postgres psql -d visionguard_db -c "GRANT CREATE ON SCHEMA public TO visionguard_user;"
```

Then re-run:

```bash
python -c "from app.db.base import init_db; init_db(); print('DB tables created (or already existed).')"
```

---

## Common issues

### `psql: command not found`
Install the client tools:

```bash
sudo apt install -y postgresql-client
```

### `password authentication failed`
Wrong password in `.env`.

### `connection refused`
Postgres service not running:

```bash
sudo systemctl status postgresql --no-pager || sudo service postgresql status
```

---

If you paste the first DB error line after restarting (just the first line, not the whole stack trace), I’ll pinpoint what step is missing.