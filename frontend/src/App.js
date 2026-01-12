import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import PasswordChange from './components/PasswordChange';
import PasswordReset from './components/PasswordReset';
import PhotoGallery from './components/PhotoGallery';
import PhotoUpload from './components/PhotoUpload';

// Configure axios defaults
axios.defaults.baseURL = 'http://localhost:8000';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in
    const token = localStorage.getItem('access_token');
    const userData = localStorage.getItem('user_data');
    
    if (token && userData) {
      setUser(JSON.parse(userData));
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    setLoading(false);
  }, []);

  const handleLogin = (token, userData) => {
    localStorage.setItem('access_token', token);
    localStorage.setItem('user_data', JSON.stringify(userData));
    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_data');
    delete axios.defaults.headers.common['Authorization'];
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        {user && (
          <nav className="navbar">
            <div className="navbar-content">
              <h1>Social Media</h1>
              <div>
                <span style={{ marginRight: '20px' }}>Welcome, {user.username}!</span>
                <Link to="/dashboard">Dashboard</Link>
                <Link to="/photos">Photos</Link>
                <Link to="/upload">Upload</Link>
                <Link to="/password-change">Change Password</Link>
                <button 
                  onClick={handleLogout} 
                  className="btn btn-secondary"
                  style={{ marginLeft: '20px' }}
                >
                  Logout
                </button>
              </div>
            </div>
          </nav>
        )}

        <div className="container">
          <Routes>
            <Route 
              path="/login" 
              element={user ? <Navigate to="/dashboard" /> : <Login onLogin={handleLogin} />} 
            />
            <Route 
              path="/register" 
              element={user ? <Navigate to="/dashboard" /> : <Register />} 
            />
            <Route 
              path="/password-reset" 
              element={<PasswordReset />} 
            />
            <Route 
              path="/dashboard" 
              element={user ? <Dashboard user={user} /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/password-change" 
              element={user ? <PasswordChange /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/photos" 
              element={user ? <PhotoGallery /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/upload" 
              element={user ? <PhotoUpload /> : <Navigate to="/login" />} 
            />
            <Route 
              path="/" 
              element={<Navigate to={user ? "/dashboard" : "/login"} />} 
            />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
