import React, { useState, useEffect } from 'react';
import axios from 'axios';

function PhotoGallery() {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchPhotos();
  }, [filter]);

  const fetchPhotos = async () => {
    setLoading(true);
    try {
      const endpoint = filter === 'all' 
        ? '/api/user-photos/' 
        : `/api/user-photos/${filter}/`;
      
      const response = await axios.get(endpoint);
      setPhotos(response.data);
    } catch (err) {
      setError('Failed to load photos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (photoId) => {
    if (!window.confirm('Are you sure you want to delete this photo?')) {
      return;
    }

    try {
      await axios.delete(`/api/user-photos/${photoId}/`);
      setPhotos(photos.filter(p => p.id !== photoId));
    } catch (err) {
      alert('Failed to delete photo');
    }
  };

  if (loading) return <div className="loading">Loading photos...</div>;

  return (
    <div>
      <div className="card">
        <h2>Photo Gallery</h2>
        <div style={{ marginBottom: '20px' }}>
          <label style={{ marginRight: '10px' }}>Filter:</label>
          <select 
            value={filter} 
            onChange={(e) => setFilter(e.target.value)}
            style={{ padding: '5px 10px' }}
          >
            <option value="all">All Photos</option>
            <option value="avatar">Avatar</option>
            <option value="personal_galery">Personal Gallery</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>

      {error && <div className="error">{error}</div>}

      {photos.length === 0 ? (
        <div className="card">
          <p>No photos found. Upload your first photo!</p>
        </div>
      ) : (
        <div className="photo-grid">
          {photos.map((photo) => (
            <div key={photo.id} className="photo-item">
              <img 
                src={`http://localhost:8000${photo.image}`} 
                alt={`Photo ${photo.id}`}
              />
              <div className="photo-item-info">
                <p><strong>Type:</strong> {photo.photo_type}</p>
                <p><small>Uploaded: {new Date(photo.uploaded_at).toLocaleDateString()}</small></p>
                <button 
                  onClick={() => handleDelete(photo.id)}
                  className="btn btn-danger"
                  style={{ marginTop: '10px', width: '100%' }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PhotoGallery;
