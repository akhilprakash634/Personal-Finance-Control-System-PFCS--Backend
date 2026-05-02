# 🚀 PFCS Deployment Guide

This guide covers how to deploy the **Personal Finance Control System (PFCS)** using Docker, Supabase, and your custom domain.

## 📋 Prerequisites
- **Docker** and **Docker Compose** installed on your server.
- A **Supabase** account (for the database).
- A **Google Cloud Console** project (for Google Auth).

---

## ⚙️ 1. Environment Configuration

### Backend (`backend/.env`)
Create a `.env` file in the `backend/` directory:
```env
PROJECT_NAME="Personal Finance Management System"
API_V1_STR="/api/v1"

# Supabase Connection (Use Transaction/Pooling Mode for Production)
SQLALCHEMY_DATABASE_URL="postgresql://user.id:password@host.pooler.supabase.com:6543/postgres"

# JWT Security
SECRET_KEY="generate-a-long-random-string-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Google OAuth
GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
```

### Frontend (`frontend/.env`)
Create a `.env` file in the `frontend/` directory:
```env
# Leave empty for Docker/Production (it uses relative paths)
VITE_API_URL=""
VITE_GOOGLE_CLIENT_ID="your-google-client-id.apps.googleusercontent.com"
```

---

## ☁️ 3. AWS Lightsail Step-by-Step Deployment

Follow these steps once you have SSH access to your Lightsail instance:

### Step 1: Clone the Project
```bash
git clone <your-repo-url>
cd Personal-Finance-Control-System-PFCS
```

### Step 2: Set up Environment Files
Create the `.env` files exactly as shown in Section 1 using `nano` or `vi`:
```bash
nano backend/.env
# Paste backend config, then Ctrl+O, Enter, Ctrl+X

nano frontend/.env
# Paste frontend config, then Ctrl+O, Enter, Ctrl+X
```

### Step 3: Open Firewall Ports
1. Go to your **Lightsail Console**.
2. Click on your instance > **Networking**.
3. Under **IPv4 Firewall**, click "Add rule".
4. Add **HTTP (80)** and **Custom (8000)** if you want direct API access (optional).

### Step 4: Run Docker Compose
```bash
sudo docker-compose up --build -d
```

### Step 5: Verify Deployment
- Visit `http://your-instance-ip` to see the frontend.
- Visit `http://your-instance-ip/api/v1/dashboard/` to check the API.

---

## 🐳 2. Deploying with Docker (Recommended)

PFCS is fully containerized. To deploy everything, run:

```bash
docker-compose up --build -d
```

### What this does:
- **Backend**: Runs the FastAPI app on port `8000`.
- **Frontend**: Serves the React app via **Nginx** on port `80`.
- **Reverse Proxy**: Nginx automatically forwards all requests starting with `/api/v1` to the backend container.

---

## 🌐 3. Domain & SSL Setup (`finance.myassistai.in`)

If you are deploying to a live server, follow these steps to secure your connection:

### Step 1: Update CORS
In `backend/app/main.py`, ensure your domain is allowed:
```python
allow_origins=[
    "https://finance.myassistai.in",
    "http://localhost",
]
```

### Step 2: Enable HTTPS
I recommend using **Certbot** with Nginx on your host machine to handle SSL termination.

---

## 🛠️ Troubleshooting

### 1. `ModuleNotFoundError: No module named 'psycopg2'`
This happens if `psycopg2-binary` is missing from `requirements.txt`. 
**Fix**: Ensure `psycopg2-binary` is in `backend/requirements.txt` and run `docker-compose build --no-cache`.

### 2. `Network is unreachable` (Supabase Connection)
If your server doesn't support IPv6, Supabase's default port (5432) will fail.
**Fix**: Use the **Supabase Pooler** (Port 6543) as configured in your `.env`.

### 3. Google Login button not appearing
Check if the Google script is in `frontend/index.html`:
```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

---

## 📊 Monitoring Logs
To check if everything is running correctly:
```bash
docker-compose logs -f
```
---

## 🤖 4. Automatic Deployment (CI/CD)

I have set up a GitHub Actions workflow in `.github/workflows/deploy.yml`. This will automatically update your server whenever you push to the `main` branch.

### Step 1: Set up GitHub Secrets
Go to your **GitHub Repository** > **Settings** > **Secrets and variables** > **Actions** and add the following secrets:

| Secret Name | Description |
| :--- | :--- |
| `LIGHTSAIL_SSH_KEY` | The content of your `.pem` private key file. |

### Step 2: Push to GitHub
Once you push your code to GitHub, the "Deploy to Lightsail" action will trigger, pull the latest code on your server, and rebuild your Docker containers automatically.

---
