# VisionGuard Backend (Windows) — Step-by-step Run Guide

This guide is for running the **backend** (`backend-visionguard-ai/`) on **Windows** with **CPU inference**.

## 0) Requirements

- Windows 10/11
- Python 3.10+ recommended (3.11 also works if your packages support it)
- Git (optional)
- PostgreSQL (recommended for full features)

## 1) Open the backend folder

In PowerShell:

```powershell
cd "E:\He_is_enough03 X UniqoXTech X Dreams\Click_here\Academic\CSE 3200\visionguard-main\backend-visionguard-ai"
```

## 2) Create + activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## 3) Install dependencies

You already installed packages, but this is the canonical step:

```powershell
pip install -r requirements.txt
```

## 4) Put the required model files in place

Create a `models/` folder inside `backend-visionguard-ai/` (if it doesn’t exist) and add the model files referenced by the config.

By default, the backend expects:

- `models/yolov8n.pt`
- `models/yolov8n-pose.pt`
- `models/stg_nf_trained.pth`

If your filenames differ, you can override paths using environment variables (next step).

## 5) Create your `.env` for Windows (CPU)

Create a file named `.env` in `backend-visionguard-ai/` with at least:

```env
# Force CPU on Windows
DEVICE=cpu

# Model paths (defaults shown here; change if your files are elsewhere)
YOLO_MODEL_PATH=./models/yolov8n.pt
POSE_MODEL_PATH=./models/yolov8n-pose.pt
ANOMALY_MODEL_PATH=./models/stg_nf_trained.pth

# Backend server
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
ENVIRONMENT=development
DEBUG_MODE=true

# Database (PostgreSQL)
DATABASE_URL=postgresql://postgres:124@localhost:5432/visionguard_db
```

Notes:
- Even if `DEVICE` is accidentally set to `cuda:0`, the backend now **auto-falls back to CPU** when CUDA isn’t available.
- The default `DATABASE_URL` requires a local Postgres instance. If you don’t have Postgres yet, do step 6.

## 6) Start PostgreSQL (recommended)

This backend uses PostgreSQL-specific column types (e.g. `JSONB`, `ARRAY`), so SQLite will not work without code changes.

Minimal local setup options on Windows:

### Option A: Install PostgreSQL locally
- Install PostgreSQL for Windows
- Create a database named `visionguard_db`
- Ensure the username/password in `DATABASE_URL` match your local setup

### Option B: Use Docker Desktop (if you have it)

```powershell
docker run --name visionguard-postgres -e POSTGRES_PASSWORD=124 -e POSTGRES_DB=visionguard_db -p 5432:5432 -d postgres:15
```

Then keep:

```env
DATABASE_URL=postgresql://postgres:124@localhost:5432/visionguard_db
```

## 7) Run database migrations / create tables

This project includes Alembic, but also calls `Base.metadata.create_all()` on startup.

If Alembic is set up for your environment, you can run:

```powershell
alembic upgrade head
```

If migrations aren’t configured/needed, you can skip this and let startup create tables.

## 8) Run the backend

From `backend-visionguard-ai/`:

### Option A (simple)

```powershell
python main.py
```

### Option B (recommended dev server)

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 9) Verify it’s running

Open in your browser:

- http://localhost:8000/ (service info)
- http://localhost:8000/docs (Swagger UI)

## 10) Common issues (Windows)

### 1) CUDA / GPU errors
- Set `DEVICE=cpu` in `.env`.
- This repo has been patched to fall back to CPU automatically if CUDA isn’t available.

### 2) Model file not found
- Ensure model files exist under `backend-visionguard-ai/models/`
- Or set `YOLO_MODEL_PATH`, `POSE_MODEL_PATH`, `ANOMALY_MODEL_PATH` to correct locations.

### 3) Database connection errors
- Confirm PostgreSQL is running and reachable.
- Verify `DATABASE_URL` is correct.

---

If you also want a **frontend (Next.js) Windows run guide**, tell me and I’ll add a separate section/file for `visionguardai-frontend/`.
