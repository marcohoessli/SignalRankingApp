import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getQuestion, getPredictionForQuestion, createPrediction, updatePrediction } from '../services/api';
import { useAuth } from '../context/AuthContext';

const QuestionDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [question, setQuestion] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [probability, setProbability] = useState(50);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      const questionRes = await getQuestion(id);
      setQuestion(questionRes.data);

      if (user) {
        try {
          const predictionRes = await getPredictionForQuestion(id);
          setPrediction(predictionRes.data);
          setProbability(predictionRes.data.probability);
        } catch (err) {
          // No prediction yet
        }
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user) {
      navigate('/login');
      return;
    }

    setSubmitting(true);
    setMessage('');

    try {
      if (prediction) {
        await updatePrediction(prediction.id, { probability });
        setMessage('Prediction updated successfully!');
      } else {
        await createPrediction({ question_id: parseInt(id), probability });
        setMessage('Prediction submitted successfully!');
      }
      fetchData();
    } catch (error) {
      setMessage(error.response?.data?.detail || 'Error submitting prediction');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;
  if (!question) return <div className="container">Question not found</div>;

  const canPredict = question.status === 'OPEN' && new Date(question.close_time) > new Date();

  return (
    <div className="container">
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '1rem' }}>
          <h1 style={{ fontSize: '1.75rem', marginBottom: '1rem' }}>{question.title}</h1>
          <span className={`badge badge-${question.status.toLowerCase()}`}>{question.status}</span>
        </div>
        
        <p style={{ lineHeight: '1.6', marginBottom: '1rem' }}>{question.description}</p>
        
        <div style={{ display: 'flex', gap: '2rem', color: '#7f8c8d', fontSize: '0.9rem' }}>
          <div><strong>Category:</strong> {question.category}</div>
          <div><strong>Closes:</strong> {new Date(question.close_time).toLocaleString()}</div>
          {question.resolve_time && (
            <div><strong>Resolved:</strong> {new Date(question.resolve_time).toLocaleString()}</div>
          )}
        </div>

        {question.outcome !== null && (
          <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: '#ecf0f1', borderRadius: '4px' }}>
            <strong>Outcome:</strong> {question.outcome ? 'YES' : 'NO'}
          </div>
        )}
      </div>

      {user && canPredict && (
        <div className="card">
          <h2 className="card-header">{prediction ? 'Update Your Prediction' : 'Make a Prediction'}</h2>
          {message && <div className={message.includes('Error') ? 'error' : 'success'}>{message}</div>}
          
          <form onSubmit={handleSubmit}>
            <div className="probability-slider">
              <div className="probability-display">{probability}%</div>
              <input
                type="range"
                min="0"
                max="100"
                value={probability}
                onChange={(e) => setProbability(parseInt(e.target.value))}
                className="slider"
              />
              <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '0.5rem', fontSize: '0.9rem', color: '#7f8c8d' }}>
                <span>0% (Definitely NO)</span>
                <span>50% (Uncertain)</span>
                <span>100% (Definitely YES)</span>
              </div>
            </div>
            
            <button type="submit" className="btn btn-primary" disabled={submitting} style={{ width: '100%' }}>
              {submitting ? 'Submitting...' : (prediction ? 'Update Prediction' : 'Submit Prediction')}
            </button>
          </form>
        </div>
      )}

      {!user && canPredict && (
        <div className="card" style={{ textAlign: 'center' }}>
          <p>Please <a href="/login">login</a> to make a prediction</p>
        </div>
      )}

      {prediction && (
        <div className="card">
          <h2 className="card-header">Your Prediction</h2>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: '#3498db', marginBottom: '0.5rem' }}>
            {prediction.probability}%
          </div>
          <div style={{ color: '#7f8c8d', fontSize: '0.9rem' }}>
            <div>Submitted: {new Date(prediction.created_at).toLocaleString()}</div>
            {prediction.updated_at !== prediction.created_at && (
              <div>Updated: {new Date(prediction.updated_at).toLocaleString()}</div>
            )}
            {prediction.brier_score !== null && (
              <div style={{ marginTop: '0.5rem' }}>
                <strong>Brier Score:</strong> {prediction.brier_score.toFixed(4)}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default QuestionDetail;
