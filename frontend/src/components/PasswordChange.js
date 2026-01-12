import React, { useState } from 'react';
import axios from 'axios';

function PasswordChange() {
  const [formData, setFormData] = useState({
    old_password: '',
    new_password: '',
    confirm_password: '',
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (formData.new_password !== formData.confirm_password) {
      setError('New passwords do not match');
      return;
    }

    setLoading(true);

    try {
      await axios.post('/api/account/password/', {
        old_password: formData.old_password,
        new_password: formData.new_password,
      });

      setSuccess('Password changed successfully!');
      setFormData({
        old_password: '',
        new_password: '',
        confirm_password: '',
      });
    } catch (err) {
      const errorMsg = err.response?.data?.old_password?.[0] || 
                      err.response?.data?.new_password?.[0] ||
                      err.response?.data?.error ||
                      'Failed to change password';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h2>Change Password</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Current Password</label>
          <input
            type="password"
            name="old_password"
            value={formData.old_password}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>New Password</label>
          <input
            type="password"
            name="new_password"
            value={formData.new_password}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>
        <div className="form-group">
          <label>Confirm New Password</label>
          <input
            type="password"
            name="confirm_password"
            value={formData.confirm_password}
            onChange={handleChange}
            required
            disabled={loading}
          />
        </div>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Changing...' : 'Change Password'}
        </button>
      </form>
    </div>
  );
}

export default PasswordChange;
