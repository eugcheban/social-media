# Social Media Frontend

A React-based frontend for the Social Media application.

## Features

- **Authentication**
  - User registration
  - Login with JWT tokens
  - Password change for authenticated users
  - Password reset flow with OTP verification

- **Dashboard**
  - View user profile information
  - List all registered users

- **Photo Gallery**
  - View all user photos
  - Filter photos by type (avatar, personal gallery, other)
  - Upload new photos
  - Delete existing photos

## Getting Started

### Prerequisites
- Node.js 18+
- Docker and Docker Compose (for containerized setup)

### Running with Docker

```bash
# From the project root
docker-compose up frontend
```

The application will be available at http://localhost:3000

### Running Locally

```bash
cd frontend
npm install
npm start
```

## Project Structure

```
frontend/
├── public/          # Static files
├── src/
│   ├── components/  # React components
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Dashboard.js
│   │   ├── PasswordChange.js
│   │   ├── PasswordReset.js
│   │   ├── PhotoGallery.js
│   │   └── PhotoUpload.js
│   ├── App.js       # Main application component
│   ├── index.js     # Entry point
│   └── index.css    # Global styles
└── package.json
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000`:

- `/api/token/` - JWT token authentication
- `/account/users/` - User management
- `/account/account/password/` - Password change
- `/account/account/password-reset/*` - Password reset flow
- `/photo/user-photos/` - Photo management

## Environment Variables

- `REACT_APP_API_URL` - Backend API URL (default: http://localhost:8000)

## Development

The application uses:
- React Router for navigation
- Axios for API calls
- JWT tokens stored in localStorage for authentication
