# VisionGuard AI

VisionGuard AI is a real-time video intelligence system for retail security and operational monitoring.
It ingests live camera streams, runs AI-based person/behavior analysis, and surfaces anomalies through a web dashboard and Telegram alerts.

## Demo

- Watch: [demo_video.mp4](demo_video.mp4)

## What It Does

- **Live feed monitoring** with real-time overlays (detections, bounding boxes)
- **Anomaly detection pipeline** (pose + temporal modeling) to flag suspicious behavior
- **Owl Eye (Sentry Mode)** for intrusion-style alerts when staff are away
- **Alerts & notifications**
  - WebSocket alerts to the frontend
  - Optional Telegram notifications per shop (when configured)
- **Incident storage**
  - Saves anomaly metadata to the database
  - Stores annotated frames for later review and feedback

## High-Level Architecture

- **Frontend (Next.js)**: [visionguardai-frontend/](visionguardai-frontend/)
  - UI dashboards, live feed, suspicious activity review
  - WebRTC to stream video to backend
  - WebSocket connection for real-time alerts and acknowledgments

- **Backend (FastAPI)**: [backend-visionguard-ai/](backend-visionguard-ai/)
  - WebRTC signaling + frame ingestion
  - AI pipeline (person detection → tracking → pose → anomaly model)
  - WebSocket alert broadcasting
  - Database persistence (anomalies + training feedback)
  - Telegram integration (optional)

## Repository Structure

- [backend-visionguard-ai/](backend-visionguard-ai/) — FastAPI backend + AI pipeline + DB + Telegram
- [visionguardai-frontend/](visionguardai-frontend/) — Next.js dashboard + WebRTC/WebSocket client
- [report/](report/) — project report chapters
- [tesing/](tesing/) — lightweight tests and outputs

## Quick Start (Recommended Reading)

This repo already contains environment and run guides; start here:

- Backend setup and run: [backend-visionguard-ai/docs/HOW_TO_RUN.md](backend-visionguard-ai/docs/HOW_TO_RUN.md)
- Windows notes: [backend-visionguard-ai/docs/HOW_TO_RUN_WINDOWS.md](backend-visionguard-ai/docs/HOW_TO_RUN_WINDOWS.md)
- Environment setup: [backend-visionguard-ai/docs/ENVIRONMENT_SETUP.md](backend-visionguard-ai/docs/ENVIRONMENT_SETUP.md)
- WebRTC/WebSocket architecture: [backend-visionguard-ai/docs/WEBRTC_WEBSOCKET_ARCHITECTURE.md](backend-visionguard-ai/docs/WEBRTC_WEBSOCKET_ARCHITECTURE.md)

## Configuration

Common configuration is done via environment variables.
See:

- [backend-visionguard-ai/app/config.py](backend-visionguard-ai/app/config.py)
- [backend-visionguard-ai/docs/AUTH_SETUP.md](backend-visionguard-ai/docs/AUTH_SETUP.md)

## Notes

- This project can save annotated anomaly frames to disk under `backend-visionguard-ai/anomaly_frames/`.
- Telegram notifications require a bot token and a configured shop `telegram_chat_id`.

