import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { getQuestions } from '../services/api';

const Questions = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ status: '', category: '', search: '' });

  useEffect(() => {
    fetchQuestions();
  }, [filters]);

  const fetchQuestions = async () => {
    try {
      const response = await getQuestions(filters);
      setQuestions(response.data);
    } catch (error) {
      console.error('Error fetching questions:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <h1 style={{ marginBottom: '2rem' }}>Questions</h1>
      
      <div className="card" style={{ marginBottom: '2rem' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
          <div className="form-group">
            <label>Status</label>
            <select value={filters.status} onChange={(e) => setFilters({ ...filters, status: e.target.value })}>
              <option value="">All</option>
              <option value="OPEN">Open</option>
              <option value="CLOSED">Closed</option>
              <option value="RESOLVED">Resolved</option>
            </select>
          </div>
          <div className="form-group">
            <label>Category</label>
            <select value={filters.category} onChange={(e) => setFilters({ ...filters, category: e.target.value })}>
              <option value="">All</option>
              <option value="Crypto">Crypto</option>
              <option value="Tech">Tech</option>
              <option value="Politics">Politics</option>
              <option value="Sports">Sports</option>
              <option value="Other">Other</option>
            </select>
          </div>
          <div className="form-group">
            <label>Search</label>
            <input
              type="text"
              placeholder="Search questions..."
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
            />
          </div>
        </div>
      </div>

      <div className="question-list">
        {questions.map(question => (
          <Link key={question.id} to={`/questions/${question.id}`} style={{ textDecoration: 'none' }}>
            <div className="question-card">
              <div className="question-title">{question.title}</div>
              <p style={{ color: '#7f8c8d', margin: '0.5rem 0' }}>{question.description.substring(0, 150)}...</p>
              <div className="question-meta">
                <span className={`badge badge-${question.status.toLowerCase()}`}>{question.status}</span>
                <span className="badge badge-category">{question.category}</span>
                <span>Closes: {new Date(question.close_time).toLocaleDateString()}</span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Questions;
