# Neptune

Agentic learning platform — MVP v0.1

## Stack
- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS
- **Backend**: Python 3.11 + FastAPI
- **Auth + DB**: Supabase
- **AI**: Anthropic Claude API (claude-sonnet-4-20250514)

## Quick Start

### Prerequisites
- Node >= 18, Python >= 3.11
- Supabase project (free tier works)
- Anthropic API key (added in-app after first login)

### 1. Clone & install
```bash
git clone <your-repo-url>
cd neptune
```

### 2. Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # fill in values
uvicorn app.main:app --reload --port 8000
```

### 3. Frontend
```bash
cd frontend
npm install
cp .env.example .env.local      # fill in values
npm run dev
```

### 4. Supabase
1. Create a project at https://supabase.com
2. Run `supabase/migrations/001_initial_schema.sql` in the Supabase SQL editor
3. Copy your project URL and anon key into the frontend `.env.local`
4. Copy your service role key and JWT secret into the backend `.env`

### 5. First login
- Create your user account directly in the Supabase Auth dashboard
  (Authentication → Users → Add user)
- Log in at http://localhost:5173
- Go to Settings and add your Claude API key

## Environment Variables

### Frontend (`frontend/.env.local`)
| Variable | Description |
|---|---|
| `VITE_SUPABASE_URL` | Your Supabase project URL |
| `VITE_SUPABASE_ANON_KEY` | Your Supabase anon/public key |
| `VITE_API_BASE_URL` | Backend URL (default: http://localhost:8000) |

### Backend (`backend/.env`)
| Variable | Description |
|---|---|
| `SUPABASE_URL` | Your Supabase project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Service role key (keep secret) |
| `SUPABASE_JWT_SECRET` | JWT secret from Supabase dashboard |

## Project Structure
```
neptune/
├── frontend/          React + TypeScript app
├── backend/           FastAPI app
├── supabase/
│   └── migrations/    SQL schema files
└── README.md
```
