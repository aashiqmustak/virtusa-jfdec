# Deploying to Vercel (Frontend) & Cloud Backend (Docker)

Your application is architected into two main layers:
1. **Frontend (`client`)**: Vue 3 + Vite SPA — **Hosted on Vercel**
2. **Backend (`server`) & Database (`db`)**: Python Litestar + PostgreSQL + Docker — **Hosted on a container platform (Render, Railway, Fly.io, or VPS)**

---

## Part 1: Deploying the Backend & Database (Docker)

Because Vercel is a serverless platform that cannot run Docker daemons, background workers, or PostgreSQL containers, your Docker backend runs on a container platform.

### Option A: 1-Click via Render (Recommended)
1. **Create PostgreSQL Database on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) -> **New +** -> **PostgreSQL**.
   - Note the **Internal Database URL** (or External URL).

2. **Create Web Service for the Backend API**:
   - In Render, click **New +** -> **Web Service**.
   - Connect your Git repository.
   - Set **Root Directory**: `msme` (or repo root)
   - Set **Runtime**: `Docker`
   - Set **Docker Command / Dockerfile Path**: `server/Dockerfile`
   - Set **Environment Variables**:
     - `DATABASE_URL`: Your Render Postgres connection string (e.g., `postgresql+psycopg://user:password@host/dbname`)
     - `ANALYST_TOKEN`: A secret token for analyst access
     - `REVIEWER_TOKEN`: A secret token for reviewer access
     - `LLM_MODE`: `mock` (or `openai` if using OpenAI API with `OPENAI_API_KEY`)
     - `CORS_ORIGINS`: `https://your-frontend.vercel.app` (or `*` temporarily)
     - `PRIVATE_STORAGE`: `/data/uploads`
     - `POLICY_FILE`: `/workspace/policy.demo.json`
   - Attach a persistent disk for `/data/uploads` if you want uploaded files to persist across deploys.
   - Note your public backend URL: `https://your-api.onrender.com`

---

### Option B: On Any VPS / Cloud Server with Docker Compose
If you already run `docker compose`:
1. Clone the repository onto your server.
2. In `.env`, set:
   ```env
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```
3. Run:
   ```bash
   docker compose up -d
   ```
4. Put a reverse proxy (Nginx or Caddy with SSL) in front of port `8000`.

---

## Part 2: Deploying the Frontend to Vercel

### Step 1: Connect to Vercel
1. Log in to [vercel.com](https://vercel.com) and click **"Add New..."** -> **"Project"**.
2. Select your Git repository.

### Step 2: Configure Project Settings
- **Framework Preset**: `Vite`
- **Root Directory**: Click "Edit" and select `client` (or `msme/client` depending on your repo root).
- **Build and Output Settings** (Automatic defaults from Vite):
  - Build Command: `npm run build`
  - Output Directory: `dist`
  - Install Command: `npm install`

### Step 3: Add Environment Variables
In the Vercel **Environment Variables** section, add:
- **Key**: `VITE_API_BASE_URL`
- **Value**: `https://your-api.onrender.com` (Your live backend URL, **without** a trailing slash)

### Step 4: Deploy
Click **Deploy**.
Vercel will build the Vue 3 app and deploy it on a fast global edge network with automatic SSL (e.g. `https://your-project.vercel.app`).

### Step 5: Update CORS on Backend
Once Vercel gives you your live URL (e.g. `https://msme-underwriting.vercel.app`):
- Update `CORS_ORIGINS` in your backend environment variables to include your Vercel URL.
