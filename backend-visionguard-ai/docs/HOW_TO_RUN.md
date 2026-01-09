# store following models in the models/ directory
- densenet_focal_epoch2.h5
- yolov8n.pt

# store videos in the videos/ directory
- sample.mp4

# set up virtual environment (optional but recommended)
```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

# install dependencies
```bash
pip install -r requirements.txt
```


# run the application
```bash
python main.py
```

---

# Frontend (Next.js) - Run Locally

The frontend lives in `visionguardai-frontend/` and runs on `http://localhost:3000`.

## Prerequisites

- Node.js 18+ (recommended: Node 18 or 20)
- Backend already running (you said it is ✅)

## Setup & Run

```bash
cd ../visionguardai-frontend

# install dependencies
npm install

# create local env
cp .env.example .env.local

# start dev server
npm run dev
```

Open `http://localhost:3000`.

## Environment Variables

Edit `visionguardai-frontend/.env.local` if your backend is not on port 8000:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
NEXT_PUBLIC_BACKEND=http://localhost:8000
NEXT_PUBLIC_VIDEO_ID=1
```

## Notes (Windows + WSL)

- If you run the backend inside WSL and the frontend on Windows, `http://localhost:8000` usually works.
- If the frontend can’t reach the backend, ensure the backend binds to `0.0.0.0` (not only `127.0.0.1`).


