import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getQuestions, getLeaderboard } from '../services/api';

const Home = () => {
  const [questions, setQuestions] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [questionsRes, leaderboardRes] = await Promise.all([
        getQuestions({ limit: 5 }),
        getLeaderboard({ limit: 5 })
      ]);
      setQuestions(questionsRes.data);
      setLeaderboard(leaderboardRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  return (
    <div className="container">
      <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>SignalRanking</h1>
        <p style={{ fontSize: '1.25rem', color: '#7f8c8d', marginBottom: '2rem' }}>
          Skill-Based Forecasting Platform
        </p>
        <p style={{ maxWidth: '600px', margin: '0 auto 2rem', lineHeight: '1.6' }}>
          Test your forecasting skills by predicting real-world events. Build your track record,
          compete with others, and prove your analytical abilities. No gambling, no money—just pure skill.
        </p>
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center' }}>
          <Link to="/signup" className="btn btn-primary" style={{ padding: '1rem 2rem' }}>
            Get Started
          </Link>
          <Link to="/questions" className="btn btn-secondary" style={{ padding: '1rem 2rem' }}>
            Browse Questions
          </Link>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', marginTop: '2rem' }}>
        <div className="card">
          <h2 className="card-header">Recent Questions</h2>
          <div className="question-list">
            {questions.map(q => (
              <Link key={q.id} to={`/questions/${q.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                <div style={{ padding: '1rem', borderBottom: '1px solid #ecf0f1' }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>{q.title}</div>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    <span className={`badge badge-${q.status.toLowerCase()}`}>{q.status}</span>
                    <span className="badge badge-category">{q.category}</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>
          <Link to="/questions" style={{ display: 'block', textAlign: 'center', marginTop: '1rem', color: '#3498db' }}>
            View All Questions →
          </Link>
        </div>

        <div className="card">
          <h2 className="card-header">Top Forecasters</h2>
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>Name</th>
                <th>Brier Score</th>
              </tr>
            </thead>
            <tbody>
              {leaderboard.map((user, idx) => (
                <tr key={user.id}>
                  <td>
                    <span className={`rank-badge rank-${idx < 3 ? idx + 1 : 'other'}`}>
                      {idx + 1}
                    </span>
                  </td>
                  <td>{user.name}</td>
                  <td>{user.avg_brier_score?.toFixed(3) || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
          <Link to="/leaderboard" style={{ display: 'block', textAlign: 'center', marginTop: '1rem', color: '#3498db' }}>
            View Full Leaderboard →
          </Link>
        </div>
      </div>

      <div className="card" style={{ marginTop: '2rem' }}>
        <h2 className="card-header">How It Works</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem' }}>
          <div>
            <h3 style={{ color: '#3498db', marginBottom: '0.5rem' }}>1. Choose a Question</h3>
            <p>Browse open questions about future events in crypto, tech, politics, and more.</p>
          </div>
          <div>
            <h3 style={{ color: '#3498db', marginBottom: '0.5rem' }}>2. Make Your Prediction</h3>
            <p>Assign a probability (0-100%) based on your analysis and research.</p>
          </div>
          <div>
            <h3 style={{ color: '#3498db', marginBottom: '0.5rem' }}>3. Get Scored</h3>
            <p>When the event resolves, your prediction is scored using the Brier Score formula.</p>
          </div>
          <div>
            <h3 style={{ color: '#3498db', marginBottom: '0.5rem' }}>4. Build Your Rank</h3>
            <p>Climb the leaderboard by making accurate predictions consistently.</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;
