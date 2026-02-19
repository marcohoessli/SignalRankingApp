from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User
from app.models.question import Question
from app.models.prediction import Prediction
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    
    try:
        # Create admin user
        admin = User(
            email="admin@signalranking.com",
            name="Admin User",
            password_hash=get_password_hash("admin123"),
            role="admin",
            email_verified=True
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        # Create demo users
        users = []
        for i in range(1, 6):
            user = User(
                email=f"user{i}@example.com",
                name=f"Demo User {i}",
                password_hash=get_password_hash("password123"),
                role="user",
                email_verified=True
            )
            db.add(user)
            users.append(user)
        
        db.commit()
        for user in users:
            db.refresh(user)
        
        # Create sample questions
        questions_data = [
            {
                "title": "Will Bitcoin reach $100,000 by end of 2024?",
                "description": "Bitcoin (BTC) must reach or exceed $100,000 USD on any major exchange by December 31, 2024, 23:59 UTC.",
                "category": "Crypto",
                "close_time": datetime.utcnow() + timedelta(days=300),
                "status": "OPEN"
            },
            {
                "title": "Will SpaceX successfully land humans on Mars by 2030?",
                "description": "SpaceX must successfully land at least one human on the surface of Mars by December 31, 2030.",
                "category": "Tech",
                "close_time": datetime.utcnow() + timedelta(days=2000),
                "status": "OPEN"
            },
            {
                "title": "Will AI pass the Turing Test convincingly by 2025?",
                "description": "An AI system must fool at least 50% of expert judges in a formal Turing Test by end of 2025.",
                "category": "Tech",
                "close_time": datetime.utcnow() + timedelta(days=400),
                "status": "OPEN"
            },
            {
                "title": "Will the S&P 500 exceed 6000 points in 2024?",
                "description": "The S&P 500 index must close above 6000 points on any trading day in 2024.",
                "category": "Other",
                "close_time": datetime.utcnow() + timedelta(days=300),
                "status": "OPEN"
            },
            {
                "title": "Will a major tech company announce a quantum computer breakthrough in 2024?",
                "description": "Google, IBM, Microsoft, or Amazon must announce a significant quantum computing breakthrough in 2024.",
                "category": "Tech",
                "close_time": datetime.utcnow() + timedelta(days=300),
                "status": "OPEN"
            },
            {
                "title": "Will Ethereum switch to proof-of-stake successfully? (RESOLVED)",
                "description": "Ethereum successfully completed The Merge to proof-of-stake in September 2022.",
                "category": "Crypto",
                "close_time": datetime.utcnow() - timedelta(days=500),
                "status": "RESOLVED",
                "outcome": True,
                "resolve_time": datetime.utcnow() - timedelta(days=450)
            },
            {
                "title": "Will Twitter be renamed to X? (RESOLVED)",
                "description": "Twitter was officially rebranded to X in July 2023.",
                "category": "Tech",
                "close_time": datetime.utcnow() - timedelta(days=200),
                "status": "RESOLVED",
                "outcome": True,
                "resolve_time": datetime.utcnow() - timedelta(days=150)
            },
            {
                "title": "Will the FIFA World Cup 2022 be held in winter? (RESOLVED)",
                "description": "The 2022 FIFA World Cup was held in Qatar in November-December 2022.",
                "category": "Sports",
                "close_time": datetime.utcnow() - timedelta(days=450),
                "status": "RESOLVED",
                "outcome": True,
                "resolve_time": datetime.utcnow() - timedelta(days=400)
            },
            {
                "title": "Will Apple release a VR headset by 2024? (RESOLVED)",
                "description": "Apple announced Vision Pro in June 2023.",
                "category": "Tech",
                "close_time": datetime.utcnow() - timedelta(days=250),
                "status": "RESOLVED",
                "outcome": True,
                "resolve_time": datetime.utcnow() - timedelta(days=200)
            },
            {
                "title": "Will global temperatures rise by 2°C by 2023? (RESOLVED)",
                "description": "Global temperatures did not rise by 2°C above pre-industrial levels by 2023.",
                "category": "Other",
                "close_time": datetime.utcnow() - timedelta(days=100),
                "status": "RESOLVED",
                "outcome": False,
                "resolve_time": datetime.utcnow() - timedelta(days=50)
            },
            {
                "title": "Will autonomous vehicles be widely available by 2024?",
                "description": "Fully autonomous vehicles (Level 5) must be commercially available in at least 3 major US cities.",
                "category": "Tech",
                "close_time": datetime.utcnow() + timedelta(days=300),
                "status": "OPEN"
            },
            {
                "title": "Will a cryptocurrency ETF be approved in the US by 2024?",
                "description": "The SEC must approve a spot Bitcoin or Ethereum ETF by December 31, 2024.",
                "category": "Crypto",
                "close_time": datetime.utcnow() + timedelta(days=300),
                "status": "OPEN"
            },
            {
                "title": "Will renewable energy exceed 50% of US electricity by 2025?",
                "description": "Renewable energy sources must account for more than 50% of US electricity generation in any month of 2025.",
                "category": "Other",
                "close_time": datetime.utcnow() + timedelta(days=500),
                "status": "OPEN"
            },
            {
                "title": "Will a major social media platform shut down in 2024?",
                "description": "Facebook, Instagram, Twitter/X, TikTok, or Snapchat must permanently shut down in 2024.",
                "category": "Tech",
                "close_time": datetime.utcnow() + timedelta(days=300),
                "status": "OPEN"
            },
            {
                "title": "Will lab-grown meat be sold in US supermarkets by 2025?",
                "description": "Lab-grown meat must be available for purchase in at least 100 US supermarkets by end of 2025.",
                "category": "Other",
                "close_time": datetime.utcnow() + timedelta(days=500),
                "status": "OPEN"
            }
        ]
        
        questions = []
        for q_data in questions_data:
            question = Question(**q_data, created_by=admin.id)
            db.add(question)
            questions.append(question)
        
        db.commit()
        for question in questions:
            db.refresh(question)
        
        # Create predictions for resolved questions
        import random
        resolved_questions = [q for q in questions if q.status == "RESOLVED"]
        
        for user in users:
            for question in resolved_questions:
                # Create varied predictions
                if question.outcome:
                    # For YES outcomes, vary predictions around 60-90%
                    probability = random.uniform(50, 95)
                else:
                    # For NO outcomes, vary predictions around 10-40%
                    probability = random.uniform(5, 50)
                
                prediction = Prediction(
                    user_id=user.id,
                    question_id=question.id,
                    probability=probability,
                    created_at=question.close_time - timedelta(days=10)
                )
                
                # Calculate Brier score
                outcome_value = 1.0 if question.outcome else 0.0
                prob_decimal = probability / 100.0
                prediction.brier_score = (prob_decimal - outcome_value) ** 2
                
                db.add(prediction)
                user.total_predictions += 1
                user.resolved_predictions += 1
        
        db.commit()
        
        # Calculate user stats
        from sqlalchemy import func
        for user in users:
            avg_brier = db.query(func.avg(Prediction.brier_score)).filter(
                Prediction.user_id == user.id,
                Prediction.brier_score.isnot(None)
            ).scalar()
            user.avg_brier_score = float(avg_brier) if avg_brier else None
        
        db.commit()
        
        # Calculate rankings
        users_with_scores = db.query(User).filter(
            User.resolved_predictions >= 3,
            User.avg_brier_score.isnot(None)
        ).order_by(User.avg_brier_score).all()
        
        for rank, user in enumerate(users_with_scores, start=1):
            user.rank_global = rank
        
        db.commit()
        
        print("✅ Database seeded successfully!")
        print(f"Created {len(users) + 1} users (including admin)")
        print(f"Created {len(questions)} questions")
        print(f"Admin credentials: admin@signalranking.com / admin123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
