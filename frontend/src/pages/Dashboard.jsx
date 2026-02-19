import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getQuestions, getMyPredictions } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const [openQuestions, setOpenQuestions] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [questionsRes, predictionsRes] = await Promise.all([
        getQuestions({ status: 'OPEN', limit: 10 }),
        getMyPredictions()
      ]);
      setOpenQuestions(questionsRes.data);
      setPredictions(predictionsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <h1 style={{ marginBottom: '2rem' }}>Dashboard</h1>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3498db' }}>{user.total_predictions}</div>
          <div style={{ color: '#7f8c8d' }}>Total Predictions</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#2ecc71' }}>{user.resolved_predictions}</div>
          <div style={{ color: '#7f8c8d' }}>Resolved</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#f39c12' }}>
            {user.avg_brier_score?.toFixed(3) || 'N/A'}
          </div>
          <div style={{ color: '#7f8c8d' }}>Avg Brier Score</div>
        </div>
        <div className="card" style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#e74c3c' }}>
            {user.rank_global || 'Unranked'}
          </div>
          <div style={{ color: '#7f8c8d' }}>Global Rank</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        <div className="card">
          <h2 className="card-header">Open Questions</h2>
          <div className="question-list">
            {openQuestions.map(q => (
              <Link key={q.id} to={`/questions/${q.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                <div style={{ padding: '1rem', borderBottom: '1px solid #ecf0f1' }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '0.5rem' }}>{q.title}</div>
                  <span className="badge badge-category">{q.category}</span>
                </div>
              </Link>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="card-header">Your Recent Predictions</h2>
          <div>
            {predictions.slice(0, 10).map(p => (
              <div key={p.id} style={{ padding: '1rem', borderBottom: '1px solid #ecf0f1' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 'bold' }}>{p.probability}%</div>
                    <div style={{ fontSize: '0.85rem', color: '#7f8c8d' }}>
                      Question #{p.question_id}
                    </div>
                  </div>
                  {p.brier_score !== null && (
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '0.85rem', color: '#7f8c8d' }}>Brier Score</div>
                      <div style={{ fontWeight: 'bold' }}>{p.brier_score.toFixed(4)}</div>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
