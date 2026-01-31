# Hots - Tech Trend Tracker 🔥

[![Live Demo](https://img.shields.io/badge/demo-online-green.svg)](https://trael8mykr1f.vercel.app/)
![Tech Stack](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue)
![Tech Stack](https://img.shields.io/badge/Backend-FastAPI-green)
![Tech Stack](https://img.shields.io/badge/Database-Supabase-orange)

> **🌟 Live Demo:** [https://trael8mykr1f.vercel.app/](https://trael8mykr1f.vercel.app/)
> 
> *Note: The demo is hosted on Vercel. Feel free to register a test account (username/password only) to experience the full features including favorites.*

Hots is a modern full-stack web application designed to help developers stay updated with the latest technology trends. It aggregates trending GitHub projects, Computer Vision papers from ArXiv, and top stories from Hacker News into a single, clean interface.

## ✨ Features

- **GitHub Trending**: Real-time crawling of GitHub's trending page to find the hottest repositories across different languages.
- **Academic Papers**: Daily updates of the latest Computer Vision (CV) papers from ArXiv.
- **Tech News**: Top stories from Hacker News.
- **User System**: 
  - Simplified **Username/Password** authentication (No email required).
  - User Profiles.
- **Favorites**: Save your favorite projects and papers to your personal collection.
- **Responsive Design**: Built with Tailwind CSS for a mobile-friendly experience.

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Routing**: React Router DOM

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database Client**: Supabase Python Client
- **Crawlers**: 
  - `httpx` (Async HTTP client)
  - `BeautifulSoup4` (HTML parsing)
  - `feedparser` (RSS/Atom parsing)
- **Validation**: Pydantic

### Database & Auth
- **Provider**: Supabase (PostgreSQL)
- **Auth**: Supabase Auth (Customized for Username-only login)
- **Storage**: Postgres Tables with Row Level Security (RLS)

## 🚀 Getting Started

### Prerequisites
- Node.js 18+
- Python 3.10+
- A Supabase account

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/hots.git
cd hots
```

### 2. Supabase Configuration
1.  Create a new project on [Supabase](https://supabase.com).
2.  Go to **Project Settings -> API** and copy your `Project URL` and `anon public key`.
3.  Go to **Authentication -> Providers -> Email**:
    *   **Enable** "Enable Email provider".
    *   **Disable** "Confirm email".
4.  Run the migration scripts in your Supabase SQL Editor (found in `supabase/migrations/`) to set up the database schema:
    *   `20240131000000_init_schema.sql`
    *   `20240131000001_add_user_trigger.sql` (Optional, logic moved to backend)
    *   `20240131000002_remove_email_column.sql`
    *   `20240131000003_change_favorites_item_id_type.sql`

### 3. Backend Setup
1.  Navigate to the `api` directory:
    ```bash
    cd api
    ```
2.  Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file in the `api` directory (or root) with your Supabase credentials:
    ```env
    SUPABASE_URL=your_supabase_url
    SUPABASE_KEY=your_supabase_service_role_key
    ```
    *Note: For the backend to bypass email restrictions and create users, you MUST use the `service_role_key` here, NOT the anon key.*

5.  Run the server:
    ```bash
    uvicorn main:app --reload
    # or
    python -m uvicorn main:app --port 8000
    ```

### 4. Frontend Setup
1.  Navigate to the root directory (where `package.json` is):
    ```bash
    cd ..
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Run the development server:
    ```bash
    npm run dev
    ```
4.  Open [http://localhost:5173](http://localhost:5173) in your browser.

## 🕷️ Crawlers
The backend includes built-in crawlers. To manually trigger a crawl:
```bash
# Powershell
Invoke-WebRequest -Method POST -Uri http://localhost:8000/api/admin/crawl
# Curl
curl -X POST http://localhost:8000/api/admin/crawl
```

## 📦 Deployment

### Frontend (Vercel/Netlify)
1.  Push your code to GitHub.
2.  Import the project into Vercel.
3.  Set the Build Command to `npm run build`.
4.  Set the Output Directory to `dist`.

### Backend (Render/Railway)
1.  Push your code to GitHub.
2.  Create a new Web Service on Render/Railway.
3.  Set the Root Directory to `api`.
4.  Set the Build Command to `pip install -r requirements.txt`.
5.  Set the Start Command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
6.  Add your `SUPABASE_URL` and `SUPABASE_KEY` to the environment variables.

## 📄 License

This project is licensed under the MIT License.
