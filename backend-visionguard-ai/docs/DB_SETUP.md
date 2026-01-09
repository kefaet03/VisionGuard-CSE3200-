# Database Setup (PostgreSQL) — VisionGuard

This backend uses **PostgreSQL + SQLAlchemy**.

Important: the backend will start even if the database is down, but **auth/shop/anomaly features will break** until the DB connects.

## 1) Create a `.env` file

In `backend-visionguard-ai/`, copy the template and edit it:

```bash
cp .env.example .env
```

Then update `DATABASE_URL` to match your Postgres credentials:

```env
# Format: postgresql://username:password@host:port/database
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/visionguard_db
```

Notes:
- If your password has special characters, URL-encode it (e.g. `@` → `%40`).
- Default port is `5432` unless you changed it.

## 2) Make sure Postgres is actually running

If you want the simplest setup (recommended for this repo in WSL), follow:
- [docs/DB_SETUP_WSL.md](docs/DB_SETUP_WSL.md)

### If Postgres is running on Windows (pgAdmin)
- pgAdmin is only the GUI — the **Postgres server** must be installed and running.
- Verify in Windows Services that **PostgreSQL** service is `Running`.

### If backend runs in WSL but Postgres runs on Windows
`localhost` inside WSL might not point to Windows Postgres.

Try this:
1. Start with `host=localhost` in `DATABASE_URL`.
2. If you get `Connection refused`, use the Windows host IP from WSL:

```bash
cat /etc/resolv.conf | grep nameserver
```

Take that IP (example `172.28.112.1`) and set:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@172.28.112.1:5432/visionguard_db
```

## 3) Create a DB user (recommended)

You said you created a database named `visionguard_db` in pgAdmin. Good.

Next, create a dedicated login role and grant access (run in pgAdmin Query Tool):

```sql
CREATE USER visionguard_user WITH PASSWORD 'strong_password_here';
GRANT ALL PRIVILEGES ON DATABASE visionguard_db TO visionguard_user;
```

Then update `.env`:

```env
DATABASE_URL=postgresql://visionguard_user:strong_password_here@localhost:5432/visionguard_db
```

## 4) Create tables

This repo currently creates tables on startup via `init_db()` (SQLAlchemy `Base.metadata.create_all`).

So:
1. Make sure your `.env` is correct
2. Restart the backend

When it connects, you should see a log like:
- `✓ Database initialized successfully`

If you don’t see it, you’ll see:
- `✗ Failed to initialize database: ...`

That error message is your best clue (password wrong, role missing, host unreachable, etc).

## 5) Quick troubleshooting

### “password authentication failed for user …”
- Wrong password in `DATABASE_URL`
- Or you’re connecting as the wrong user

### “role … does not exist”
- Create the role in pgAdmin, or use an existing one like `postgres`

### “connection refused”
- Postgres service isn’t running
- Wrong host/port
- If backend is in WSL and Postgres is on Windows, use the Windows host IP (see section 2)

### “relation \"users\" does not exist”
- DB connection works, but tables were not created yet.
- Follow the one-time init instructions in [docs/DB_SETUP_WSL.md](docs/DB_SETUP_WSL.md).

### “database … does not exist”
- You created the DB in pgAdmin, but the name in `DATABASE_URL` doesn’t match exactly

## 6) Recommended verification (pgAdmin)

After the backend starts successfully, in pgAdmin:
- Open `visionguard_db` → `Schemas` → `public` → `Tables`
- You should see tables like `users`, `shops`, etc. (names depend on model definitions).

---

If you paste the exact DB error line from the backend logs (the one after `Failed to initialize database:`), I can tell you the precise fix.