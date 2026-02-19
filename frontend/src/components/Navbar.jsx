import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { user, logoutUser } = useAuth();

  return (
    <nav className="navbar">
      <div className="navbar-content">
        <Link to="/" className="navbar-brand">SignalRanking</Link>
        <div className="navbar-links">
          <Link to="/questions">Questions</Link>
          <Link to="/leaderboard">Leaderboard</Link>
          {user ? (
            <>
              <Link to="/dashboard">Dashboard</Link>
              {user.role === 'admin' && <Link to="/admin">Admin</Link>}
              <Link to="/profile">Profile</Link>
              <button onClick={logoutUser} className="btn btn-secondary">Logout</button>
            </>
          ) : (
            <>
              <Link to="/login">Login</Link>
              <Link to="/signup">Sign Up</Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
