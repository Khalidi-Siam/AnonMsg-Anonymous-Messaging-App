# AnonMsg - Project Features & Implementation

## Project Overview
AnonMsg is a secure, anonymous messaging application built with Django that implements end-to-end encryption using AES-256. The application allows users to send and receive encrypted messages while maintaining privacy and security.

## Architecture

### Technology Stack
- **Backend**: Django 5.2 (Python web framework)
- **Database**: SQLite3 (development), easily configurable for PostgreSQL/MySQL
- **Encryption**: AES-256 with EAX mode using pycryptodome
- **Frontend**: HTML5, CSS3, JavaScript with Tailwind CSS
- **Authentication**: Django's built-in authentication with custom user model

### Project Structure
```
AnonMsg/
├── AnonMsg/                 # Main project configuration
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL routing
│   ├── key_manager.py     # Encryption utilities
│   └── wsgi.py            # WSGI configuration
├── user_app/              # User management app
├── messenger_app/         # Messaging functionality
├── templates/             # HTML templates
├── static/               # Static files (CSS, JS, images)
└── manage.py             # Django management script
```

## Core Features

### 1. User Authentication & Management

#### Custom User Model (`user_app/models.py`)
- **Custom User Implementation**: Extends Django's AbstractBaseUser
- **Encrypted Email Storage**: Email addresses are encrypted using AES-256
- **Encrypted Profile Pictures**: User avatars stored with encryption
- **Username-based Authentication**: Primary authentication field

**Key Components:**
```python
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email_encrypted = models.BinaryField()
    email_nonce = models.BinaryField()
    profile_picture_encrypted = models.BinaryField()
    profile_picture_nonce = models.BinaryField()
```

**Security Features:**
- PBKDF2 with SHA256 password hashing (Django default)
- Unique username requirement
- Encrypted sensitive data storage

#### User Registration (`user_app/views.py`)
- **Validation**: Username uniqueness, email uniqueness, password confirmation
- **Data Processing**: Capitalizes usernames, lowercases emails
- **Security**: Encrypted email storage during registration
- **Error Handling**: Comprehensive form validation with user feedback

#### User Authentication
- **Login System**: Username and password based
- **Session Management**: Django's built-in session framework
- **Access Control**: Login required decorators for protected views

#### Profile Management
- **Profile Viewing**: Displays username, encrypted email, profile picture
- **Profile Editing**: Upload and update encrypted profile pictures
- **Image Handling**: Base64 encoding for image display
- **Default Avatar**: Fallback to default profile image

### 2. Encryption System

#### AES-256 Encryption (`AnonMsg/key_manager.py`)
- **Algorithm**: AES-256 in EAX mode
- **Key Management**: 32-byte keys stored in environment variables
- **Nonce Generation**: Random 16-byte nonces for each encryption
- **Authentication**: Built-in authentication tag verification

**Encryption Process:**
1. Generate random nonce (16 bytes)
2. Create AES cipher with EAX mode
3. Encrypt data and generate authentication tag
4. Combine ciphertext and tag for storage
5. Store nonce separately for decryption

**Security Benefits:**
- **Authenticated Encryption**: Prevents tampering
- **Unique Nonces**: Each encryption uses different nonce
- **Key Separation**: Encryption key stored separately from database
- **Forward Secrecy**: Past messages remain secure if current key is compromised

#### Key Management (`initialize_key.py`)
- **Key Generation**: Cryptographically secure random key generation
- **Base64 Encoding**: Safe storage in environment files
- **One-time Setup**: Prevents accidental key regeneration
- **Environment Integration**: Seamless integration with Django settings

### 3. Messaging System

#### Message Model (`messenger_app/models.py`)
- **Encrypted Content**: All message content encrypted with AES-256
- **User Relationships**: Foreign keys to sender and recipient
- **Timestamp Tracking**: Automatic timestamp for message ordering
- **Bi-directional References**: Sent and received message relationships

```python
class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages")
    recipient = models.ForeignKey(User, related_name="received_messages")
    encrypted_content = models.BinaryField()
    nonce = models.BinaryField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

#### Message Sending (`messenger_app/views.py`)
- **Recipient Validation**: Verify recipient exists
- **Content Encryption**: Automatic encryption before storage
- **AJAX Support**: Modal-based message sending
- **Error Handling**: Comprehensive error reporting
- **Redirect Logic**: Smart navigation after sending

#### Inbox Management
- **Conversation View**: Organized by conversation partners
- **Message Decryption**: Real-time decryption for display
- **Chronological Ordering**: Messages sorted by timestamp
- **User Filtering**: Filter messages by conversation partner
- **Bi-directional Display**: Shows both sent and received messages

### 4. User Interface

#### Design System
- **Framework**: Tailwind CSS for responsive design
- **Theme**: Dark/light mode support with system preference detection
- **Layout**: Glass morphism design with modern aesthetics
- **Typography**: Inter font family for clean readability

#### Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Adaptive Layout**: Flexible grid system
- **Touch-Friendly**: Appropriate touch targets
- **Cross-Browser**: Compatible with modern browsers

#### Key UI Components

**Navigation:**
- Dynamic navigation based on authentication status
- Profile picture display in navigation
- Theme toggle functionality
- Responsive hamburger menu

**Inbox Interface:**
- **Sidebar**: Conversation list with search functionality
- **Main Panel**: Message thread display
- **Compose Modal**: Inline message composition

**Forms:**
- **Registration/Login**: Clean, accessible forms
- **Validation**: Client-side and server-side validation
- **Error Display**: User-friendly error messaging
- **Success Feedback**: Confirmation messages

### 5. Security Implementation

#### Data Protection
- **Email Encryption**: User emails never stored in plaintext
- **Message Encryption**: All message content encrypted
- **Profile Picture Encryption**: User avatars encrypted
- **Database Security**: Sensitive data unreadable without decryption key

#### Authentication Security
- **Password Hashing**: PBKDF2 with SHA256 and salt
- **Session Management**: Secure session handling
- **CSRF Protection**: Cross-site request forgery protection
- **XFrame Protection**: Clickjacking protection

#### Key Security Features
- **Environment Variable Storage**: Encryption keys not in source code
- **Nonce Uniqueness**: Each encryption uses unique nonce
- **Error Handling**: Graceful handling of decryption failures
- **Access Control**: Login required for sensitive operations

### 6. Database Design

#### User Data Model
```sql
-- Custom User Table
user_app_user:
- id (Primary Key)
- username (Unique)
- password (Hashed)
- email_encrypted (Binary)
- email_nonce (Binary)
- profile_picture_encrypted (Binary)
- profile_picture_nonce (Binary)
- is_active (Boolean)
```

#### Message Data Model
```sql
-- Message Table
messenger_app_message:
- id (Primary Key)
- sender_id (Foreign Key to User)
- recipient_id (Foreign Key to User)
- encrypted_content (Binary)
- nonce (Binary)
- timestamp (DateTime)
```

#### Relationships
- **One-to-Many**: User to sent messages
- **One-to-Many**: User to received messages
- **Foreign Key Constraints**: Maintain referential integrity
- **Cascade Deletion**: Clean up related data on user deletion

### 7. API Endpoints

#### Authentication Endpoints
- `GET /` - Home page (redirects based on auth status)
- `GET /register/` - Registration form
- `POST /register/` - Process registration
- `GET /login/` - Login form
- `POST /login/` - Process login
- `POST /logout/` - Logout user

#### User Profile Endpoints
- `GET /profile/` - View user profile
- `GET /profile/edit/` - Edit profile form
- `POST /profile/edit/` - Update profile

#### Messaging Endpoints
- `GET /inbox/` - View inbox with conversations
- `GET /inbox/?sender=username` - Filter by conversation
- `GET /send/` - Message composition form
- `POST /send/` - Send message (supports AJAX)

### 8. Error Handling & Validation

#### Server-Side Validation
- **User Registration**: Username/email uniqueness, password confirmation
- **Message Sending**: Recipient existence, content validation
- **Profile Updates**: File type validation
- **Authentication**: Credential validation

#### Client-Side Features
- **Form Validation**: Real-time input validation
- **Error Display**: User-friendly error messages
- **Loading States**: Visual feedback during operations
- **Success Confirmations**: Clear success messaging

#### Encryption Error Handling
- **Graceful Degradation**: Fallback for decryption failures
- **Error Logging**: Detailed error information for debugging
- **User Feedback**: Informative error messages



## Future Enhancement Possibilities

### Technical Improvements
- **Real-time Messaging**: WebSocket implementation
- **Message Expiration**: Auto-delete messages after time period
- **Group Messaging**: Multi-user conversations
- **File Attachments**: Encrypted file sharing
- **Two-Factor Authentication**: Additional security layer

### User Experience
- **Progressive Web App**: PWA capabilities
- **Advanced Search**: Message content search
- **Message Reactions**: Emoji reactions
- **Typing Indicators**: Real-time typing status
- **Active Status**: User active or not like **Messenger**

### Security Enhancements
- **HTTPS Implementation**: Ensures secure communication between clients and the server
- **HMAC Implementation**: Utilizes Hash-based Message Authentication Codes (HMAC) to verify the integrity and authenticity of messages
- **Key Sharing Mechanism**: Implements a secure key exchange protocol (e.g., Diffie-Hellman or Elliptic Curve Diffie-Hellman) to establish shared encryption keys between users for end-to-end encrypted messaging. This ensures that only the communicating parties can read the exchanged messages.
- **Perfect Forward Secrecy**: Rotating encryption keys
- **Zero-Knowledge Architecture**: Server cannot decrypt messages
- **Signal Protocol**: Advanced cryptographic protocol

## Conclusion

AnonMsg demonstrates a robust implementation of secure messaging with Django, featuring comprehensive encryption, user management, and modern web design. The application successfully balances security, usability, and performance while maintaining a clean, maintainable codebase.
