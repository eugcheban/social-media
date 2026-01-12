import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function PhotoUpload() {
  const [file, setFile] = useState(null);
  const [photoType, setPhotoType] = useState('other');
  const [preview, setPreview] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      setPreview(URL.createObjectURL(selectedFile));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('image', file);
    formData.append('photo_type', photoType);

    try {
      await axios.post('/api/user-photos/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      alert('Photo uploaded successfully!');
      navigate('/photos');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to upload photo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card" style={{ maxWidth: '600px', margin: '0 auto' }}>
      <h2>Upload Photo</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Photo Type</label>
          <select
            value={photoType}
            onChange={(e) => setPhotoType(e.target.value)}
            disabled={loading}
            style={{ width: '100%', padding: '10px' }}
          >
            <option value="avatar">Avatar</option>
            <option value="personal_galery">Personal Gallery</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="form-group">
          <label>Select Photo</label>
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            required
            disabled={loading}
          />
        </div>

        {preview && (
          <div style={{ marginBottom: '20px' }}>
            <img 
              src={preview} 
              alt="Preview" 
              style={{ 
                maxWidth: '100%', 
                maxHeight: '300px', 
                borderRadius: '8px' 
              }} 
            />
          </div>
        )}

        {error && <div className="error">{error}</div>}

        <button 
          type="submit" 
          className="btn btn-primary" 
          disabled={loading || !file}
        >
          {loading ? 'Uploading...' : 'Upload Photo'}
        </button>
      </form>
    </div>
  );
}

export default PhotoUpload;
