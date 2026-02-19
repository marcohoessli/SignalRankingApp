import React, { useEffect, useState } from 'react';
import { getLeaderboard } from '../services/api';

const Leaderboard = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const response = await getLeaderboard({ limit: 100 });
      setUsers(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="container">
      <h1 style={{ marginBottom: '2rem' }}>Leaderboard</h1>
      
      <div className="card">
        <table className="leaderboard-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Name</th>
              <th>Avg Brier Score</th>
              <th>Total Predictions</th>
              <th>Resolved</th>
            </tr>
          </thead>
          <tbody>
            {users.map((user, idx) => (
              <tr key={user.id}>
                <td>
                  <span className={`rank-badge rank-${idx < 3 ? idx + 1 : 'other'}`}>
                    {idx + 1}
                  </span>
                </td>
                <td><strong>{user.name}</strong></td>
                <td>{user.avg_brier_score?.toFixed(4) || 'N/A'}</td>
                <td>{user.total_predictions}</td>
                <td>{user.resolved_predictions}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Leaderboard;
