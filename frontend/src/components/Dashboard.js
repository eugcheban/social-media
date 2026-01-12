import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Dashboard({ user }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get('/api/users/');
      setUsers(response.data);
    } catch (err) {
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div>
      <div className="card">
        <h2>Welcome, {user.username}!</h2>
        <p><strong>Email:</strong> {user.email}</p>
        <p><strong>Account Status:</strong> {user.is_active ? 'Active' : 'Inactive'}</p>
        <p><strong>Member since:</strong> {new Date(user.date_joined).toLocaleDateString()}</p>
      </div>

      <div className="card">
        <h3>All Users</h3>
        {error && <div className="error">{error}</div>}
        <ul className="user-list">
          {users.map((u) => (
            <li key={u.id} className="user-item">
              <div>
                <strong>{u.username}</strong>
                <br />
                <small>{u.email}</small>
              </div>
              <div>
                <span style={{ 
                  padding: '5px 10px', 
                  borderRadius: '4px', 
                  background: u.is_active ? '#d4edda' : '#f8d7da',
                  color: u.is_active ? '#155724' : '#721c24',
                  fontSize: '12px'
                }}>
                  {u.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
