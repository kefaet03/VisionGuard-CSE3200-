# VisionGuard AI

Real-time video intelligence for monitoring live camera feeds, detecting suspicious activity, and delivering alerts to a web dashboard and Telegram.

- Demo video: [demo_video](output01.mp4)

## Table of contents

- [Overview](#overview)
- [Key features](#key-features)
- [Architecture](#architecture)
- [Quick start](#quick-start)
  - [Backend (FastAPI)](#backend-fastapi)
  - [Frontend (Next.js)](#frontend-nextjs)
- [Configuration](#configuration)
- [Telegram alerts](#telegram-alerts)
- [Project structure](#project-structure)
- [Docs](#docs)
- [License](#license)

## Overview

VisionGuard AI combines:

- A **FastAPI backend** that receives video via **WebRTC**, runs the AI pipeline, persists incidents, and pushes alerts.
- A **Next.js frontend** that provides a dashboard, live feed, and incident review.

## Key features

- **Live monitoring**: WebRTC live feed with detection overlays.
- **Anomaly detection**: Pose + temporal modeling pipeline for suspicious behavior detection.
- **Owl Eye (Sentry Mode)**: Intrusion-style alerts when a person is detected.
  - Includes **server-side per-location cooldown** to prevent alert spam (same location won’t trigger repeatedly within 2 seconds).
- **Alerts**:
  - WebSocket alerts to the frontend.
  - Optional Telegram notifications per shop (when configured).
- **Incident storage**:
  - Saves anomalies to the database.
  - Saves annotated frames under `backend-visionguard-ai/anomaly_frames/`.

## Architecture

- Frontend: [visionguardai-frontend/](visionguardai-frontend/)
  - WebRTC video → backend
  - WebSocket alerts ← backend
- Backend: [backend-visionguard-ai/](backend-visionguard-ai/)
  - WebRTC signaling + frame ingestion
  - AI pipeline: person detection → tracking → pose → anomaly model
  - WebSocket alert broadcasting
  - Database persistence + feedback storage
  - Telegram integration

## Quick start

For full details, see the repo docs. The steps below are the “happy path” for local development.

### Backend (FastAPI)

From the repository root:

```bash
cd backend-visionguard-ai

# (recommended) create & activate venv
python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

1) Put model files into `backend-visionguard-ai/models/` (or override paths via env vars):

- `models/yolov8n.pt`
- `models/yolov8n-pose.pt`
- `models/stg_nf_trained.pth`

2) Configure environment variables (commonly via `backend-visionguard-ai/.env`). Minimum useful example:

```env
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# CPU-only machines (common on Windows)
DEVICE=cpu

# Database (PostgreSQL recommended)
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/visionguard_db
```

3) Run the backend:

```bash
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- `http://localhost:8000/docs`

Windows notes: [backend-visionguard-ai/docs/HOW_TO_RUN_WINDOWS.md](backend-visionguard-ai/docs/HOW_TO_RUN_WINDOWS.md)

### Frontend (Next.js)

In a second terminal:

```bash
cd visionguardai-frontend
npm install

# create local env
cp .env.example .env.local

npm run dev
```

Open `http://localhost:3000`.

## Configuration

Backend config:

- Runtime + model settings: [backend-visionguard-ai/app/config.py](backend-visionguard-ai/app/config.py)
- Environment setup guide: [backend-visionguard-ai/docs/ENVIRONMENT_SETUP.md](backend-visionguard-ai/docs/ENVIRONMENT_SETUP.md)

Frontend config:

- Example env file: [visionguardai-frontend/.env.example](visionguardai-frontend/.env.example)
- WebRTC integration notes: [visionguardai-frontend/WEBRTC_INTEGRATION.md](visionguardai-frontend/WEBRTC_INTEGRATION.md)

## Telegram alerts

Telegram notifications are sent for alert notifications when a shop has a configured `telegram_chat_id`.

- Telegram docs: [backend-visionguard-ai/docs/TELEGRAM_INTEGRATION.md](backend-visionguard-ai/docs/TELEGRAM_INTEGRATION.md)

## Project structure

- [backend-visionguard-ai/](backend-visionguard-ai/) — FastAPI backend + AI pipeline + DB + Telegram
- [visionguardai-frontend/](visionguardai-frontend/) — Next.js dashboard + WebRTC/WebSocket client
- [report/](report/) — report chapters
- [tesing/](tesing/) — tests (smoke/unit)

## Docs

- Backend run guide: [backend-visionguard-ai/docs/HOW_TO_RUN.md](backend-visionguard-ai/docs/HOW_TO_RUN.md)
- WebRTC/WebSocket architecture: [backend-visionguard-ai/docs/WEBRTC_WEBSOCKET_ARCHITECTURE.md](backend-visionguard-ai/docs/WEBRTC_WEBSOCKET_ARCHITECTURE.md)
- WebSocket quick reference: [backend-visionguard-ai/docs/WEBSOCKET_QUICK_REFERENCE.md](backend-visionguard-ai/docs/WEBSOCKET_QUICK_REFERENCE.md)

## License

No license file is included in this repository.



