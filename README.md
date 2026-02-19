# SignalRanking

A full-stack skill-based forecasting platform where users predict real-world events using probabilities. Users are ranked by the accuracy of their predictions using the Brier Score.

**This is NOT gambling, NO money, and NO betting.** Users build a public track record and compete based on forecasting skill.

## 🎯 Features

### Core Functionality
- **Probabilistic Predictions**: Users assign probabilities (0-100%) to future events
- **Brier Score Ranking**: Predictions scored using the Brier Score formula
- **Global Leaderboard**: Users ranked by average Brier Score
- **Multiple Categories**: Crypto, Tech, Politics, Sports, and more
- **Question Lifecycle**: OPEN → CLOSED → RESOLVED states

### User Features
- Email/password authentication with JWT
- Email verification
- Password reset
- Personal dashboard with stats
- Prediction history
- Edit predictions before deadline
- Public profile pages

### Admin Features
- Create/edit/delete questions
- Close questions
- Resolve outcomes (YES/NO)
- Manage users
- View audit logs

## 🛠 Tech Stack

### Backend
- **FastAPI** (Python) - REST API
- **PostgreSQL** - Database
- **SQLAlchemy** - ORM
- **JWT** - Authentication
- **Bcrypt** - Password hashing

### Frontend
- **React** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file (copy from `.env.example`):
```bash
cp .env.example .env
```

5. Configure environment variables in `.env`:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/signalranking
JWT_SECRET_KEY=your-secret-key-here
```

6. Create database:
```bash
createdb signalranking
```

7. Run migrations (tables will be created automatically on first run):
```bash
python -m uvicorn app.main:app --reload
```

8. Seed database with demo data:
```bash
python seed_data.py
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 🚀 Running the Application

### Start Backend
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend API: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

### Start Frontend
```bash
cd frontend
npm run dev
```

Frontend: `http://localhost:3000`

## 👤 Demo Accounts

After running `seed_data.py`:

**Admin Account:**
- Email: `admin@signalranking.com`
- Password: `admin123`

**Demo Users:**
- Email: `user1@example.com` through `user5@example.com`
- Password: `password123`

## 📊 Brier Score

The Brier Score measures the accuracy of probabilistic predictions:

```
Brier Score = (p - o)²
```

Where:
- `p` = predicted probability (0-1)
- `o` = actual outcome (1 for YES, 0 for NO)

**Lower scores are better** (0 = perfect prediction, 1 = worst possible)

Examples:
- Predict 90% for YES outcome: (0.9 - 1)² = 0.01 ✅
- Predict 10% for YES outcome: (0.1 - 1)² = 0.81 ❌
- Predict 50% for any outcome: 0.25 (neutral)

## 🗂 Project Structure

```
SignalRankingApp/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Config, database, security
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utilities
│   ├── requirements.txt
│   ├── .env.example
│   └── seed_data.py
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API client
│   │   ├── context/      # React context
│   │   └── styles/       # CSS
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🔐 Security Features

- JWT-based authentication
- Bcrypt password hashing
- Rate limiting on login attempts
- CORS configuration
- Input validation
- SQL injection protection (SQLAlchemy ORM)
- XSS protection

## 📝 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `GET /api/auth/verify-email` - Verify email
- `POST /api/auth/request-password-reset` - Request password reset
- `POST /api/auth/reset-password` - Reset password

### Questions
- `GET /api/questions` - List questions (with filters)
- `GET /api/questions/{id}` - Get question details
- `POST /api/questions` - Create question (admin)
- `PUT /api/questions/{id}` - Update question (admin)
- `POST /api/questions/{id}/close` - Close question (admin)
- `POST /api/questions/{id}/resolve` - Resolve question (admin)
- `DELETE /api/questions/{id}` - Delete question (admin)

### Predictions
- `GET /api/predictions` - Get my predictions
- `POST /api/predictions` - Create prediction
- `PUT /api/predictions/{id}` - Update prediction
- `GET /api/predictions/question/{id}` - Get prediction for question

### Leaderboard
- `GET /api/leaderboard` - Get ranked users

## 🎨 UI Design

The platform features a clean, professional fintech-style interface:
- Blue/white/gray color scheme
- Data-focused layout
- Mobile responsive
- Minimal and professional

## 🚢 Deployment

### Backend Deployment
1. Set up PostgreSQL database
2. Configure environment variables
3. Run migrations
4. Deploy with Gunicorn/Uvicorn

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Deploy `dist/` folder to static hosting
3. Configure API URL

## 📄 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

This is a complete, production-ready application. Feel free to fork and customize for your needs.

## 📧 Support

For issues or questions, please open an issue on the repository.
