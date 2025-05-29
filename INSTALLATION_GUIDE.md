# AnonMsg - Installation & Setup Guide

## Overview
AnonMsg is a Django-based anonymous messaging application with end-to-end encryption using AES-256. This guide will walk you through setting up and running the project.

## Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

## Installation Steps

### 1. Clone the Repository
```cmd
git clone <repository-url>
cd AnonMsg-Anonymous-Messaging-App
```

### 2. Create Virtual Environment
```cmd
python -m venv env
```

### 3. Activate Virtual Environment
```cmd
env\Scripts\activate
```

### 4. Install Dependencies
```cmd
pip install -r requirements.txt
```

**Dependencies installed:**
- Django 5.2 (Web framework)
- pycryptodome 3.22.0 (Encryption library)
- python-dotenv 1.1.0 (Environment variable management)
- asgiref 3.8.1 (ASGI reference implementation)
- sqlparse 0.5.3 (SQL parser)
- tzdata 2025.2 (Timezone data)

### 5. Setup Environment Variables
Create a `.env` file in the project root directory:
```cmd
echo. > .env
```

Generate the AES encryption key by running:
```cmd
python initialize_key.py
```

This will create an `AES_SECRET_KEY` in your `.env` file. The key is essential for encrypting/decrypting user data.

### 6. Database Setup
Run database migrations to create the necessary tables:
```cmd
python manage.py makemigrations
python manage.py migrate
```


### 7. Run the Development Server
```cmd
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Database Information
- **Database Type**: SQLite3 (default)
- **Database File**: `db.sqlite3` (created automatically)
- **Location**: Project root directory

### Database Schema
The application uses two main apps:
- **user_app**: Custom user model with encrypted email and profile pictures
- **messenger_app**: Message model with encrypted content

## Configuration Files
- **settings.py**: Main Django configuration
- **requirements.txt**: Python dependencies
- **.env**: Environment variables (created during setup)
- **initialize_key.py**: AES key generation utility (**only for development**)

## Static Files
- **Static Directory**: `static/`
- **Template Directory**: `templates/`
- **Media Directory**: `media/` (for user uploads)

## Security Features
- AES-256 encryption for sensitive data
- PBKDF2 with SHA256 for password hashing
- Random nonce generation for each encryption
- Environment-based secret key management

## Troubleshooting

### Common Issues

1. **Virtual Environment Activation**
   ```cmd
   env\Scripts\activate
   ```

2. **Missing AES Key Error**
   - Ensure you've run `python initialize_key.py`
   - Check that `.env` file exists with `AES_SECRET_KEY`



### Logs and Debugging
- Enable DEBUG mode in `settings.py` for development
- Check console output for error messages

## Development vs Production

### Development Setup (Current)
- SQLite database
- DEBUG = True
- Local static file serving
- Development server (manage.py runserver)

### Production Considerations
- Use PostgreSQL/MySQL database
- Set DEBUG = False
- Configure proper static file serving (Nginx/Apache)
- Use WSGI server (Gunicorn, uWSGI)
- Set up proper environment variables
- Configure ALLOWED_HOSTS
- Use HTTPS for security

## Next Steps
After successful installation:
1. Visit `http://127.0.0.1:8000/`
2. Register a new account
3. Start sending encrypted messages!

For detailed feature information, see `PROJECT_FEATURES.md`.
