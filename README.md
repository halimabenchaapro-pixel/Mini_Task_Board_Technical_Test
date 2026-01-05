# Mini Task Board - Full Stack Application

A modern, full-featured task management board built with Django REST Framework and React. This application demonstrates best practices in full-stack development, including comprehensive testing, security measures, and a polished user interface.

## 🎯 Features

### Core Functionality
- ✅ **Task Management**: Create, read, update, and delete tasks
- 🎯 **Kanban Board**: Drag-and-drop tasks between columns (Backlog, In Progress, Done)
- 🔍 **Advanced Filtering**: Filter by status, priority, and search by title
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices
- 🌓 **Dark Mode**: Toggle between light and dark themes
- ⚡ **Real-time Updates**: Optimistic UI updates for instant feedback

### Enhanced UX Features
- 🚀 **Quick Add**: Add tasks directly in each column
- ⌨️ **Keyboard Shortcuts**: Ctrl/Cmd + K to quickly add tasks
- 📊 **Statistics**: View task distribution by status and priority
- 🔄 **Bulk Operations**: Update multiple tasks at once
- 🔔 **Toast Notifications**: Visual feedback for all actions
- 📄 **Pagination**: Efficient handling of large datasets

### Security Features
- 🔒 **API Key Authentication**: Secure API access
- 🛡️ **SQL Injection Protection**: Pattern-based detection and blocking
- 🚫 **XSS Protection**: Multiple layers of defense
- ⏱️ **Rate Limiting**: 100 requests per 60 seconds per IP
- 📝 **Request Logging**: Complete audit trail with IP tracking
- 🔐 **Security Headers**: XSS-Protection, X-Frame-Options, Content-Security-Policy

## 🏗️ Tech Stack

### Backend
- **Django 4.2.9** - Python web framework
- **Django REST Framework** - RESTful API toolkit
- **SQLite** - Database (easily swappable to PostgreSQL)
- **Python 3.9+** - Programming language

### Frontend
- **React 19** - UI library
- **Vite 7** - Build tool and dev server
- **Tailwind CSS 3** - Utility-first CSS framework
- **Axios** - HTTP client
- **@hello-pangea/dnd** - Drag-and-drop functionality
- **React Router** - Client-side routing

### Testing & Quality
- **Backend**: Django TestCase, coverage.py (95% coverage)
- **Frontend**: Vitest, React Testing Library (78% coverage)
- **94 backend tests** covering models, views, serializers, and middleware
- **38 frontend tests** covering components, contexts, and services

## 📋 Prerequisites

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- Git

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/halimabenchaapro-pixel/Mini_Task_Board_Technical_Test.git
cd Mini_Task_Board_Technical_Test
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin panel)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

The backend will be running at `http://127.0.0.1:8000`

### 3. Frontend Setup

```bash
# Open a new terminal and navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be running at `http://localhost:5173` (or 5174/5175 if ports are busy)

### 4. Access the Application

1. Open your browser and go to `http://localhost:5173`
2. Enter the API key: `dev-api-key-12345` (default development key)
3. Start managing your tasks!

## 🔑 Environment Configuration

### Backend (.env)
Create a `.env` file in the `backend` directory:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
API_KEY=dev-api-key-12345
```

### Frontend (.env)
Create a `.env` file in the `frontend` directory:

```env
VITE_API_URL=http://127.0.0.1:8000/api
VITE_API_KEY=dev-api-key-12345
```

## 🧪 Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate

# Run all tests
python manage.py test tasks

# Run tests with coverage
coverage run --source='tasks' manage.py test tasks
coverage report
coverage html  # Generate HTML report in htmlcov/
```

**Test Coverage: 95%**
- 94 tests covering models, views, serializers, and middleware
- All CRUD operations tested
- Security middleware validated
- Authentication and authorization tested

### Frontend Tests

```bash
cd frontend

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run tests with UI
npm run test:ui
```

**Test Coverage: 78%**
- 38 tests covering components, contexts, and services
- Button component: 100% coverage
- AuthContext: 100% coverage
- User interactions and state management tested

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api
```

### Authentication
All requests require the `X-API-KEY` header:
```
X-API-KEY: dev-api-key-12345
```

### Endpoints

#### Tasks

**List all tasks**
```http
GET /api/tasks/
```

Query parameters:
- `page`: Page number (default: 1)
- `page_size`: Items per page (max: 100)
- `status`: Filter by status (BACKLOG, IN_PROGRESS, DONE)
- `priority`: Filter by priority (LOW, MEDIUM, HIGH)
- `search`: Search in title and description
- `ordering`: Sort by field (e.g., `-created_at`, `priority`)
- `due_date_from`: Filter tasks due after date
- `due_date_to`: Filter tasks due before date
- `overdue`: Show only overdue tasks (true/false)

**Create a task**
```http
POST /api/tasks/
Content-Type: application/json

{
  "title": "Task title",
  "description": "Task description",
  "status": "BACKLOG",
  "priority": "MEDIUM",
  "due_date": "2026-12-31"
}
```

**Get a task**
```http
GET /api/tasks/{id}/
```

**Update a task**
```http
PATCH /api/tasks/{id}/
Content-Type: application/json

{
  "status": "DONE"
}
```

**Delete a task**
```http
DELETE /api/tasks/{id}/
```

**Bulk update status**
```http
POST /api/tasks/bulk_update_status/
Content-Type: application/json

{
  "task_ids": [1, 2, 3],
  "status": "DONE"
}
```

**Get statistics**
```http
GET /api/tasks/statistics/
```

Response:
```json
{
  "total": 10,
  "by_status": {
    "backlog": 3,
    "in_progress": 4,
    "done": 3
  },
  "by_priority": {
    "low": 2,
    "medium": 5,
    "high": 3
  }
}
```

## 🎨 Features Showcase

### Drag and Drop
Seamlessly move tasks between columns with visual feedback and animations.

### Quick Add
Add tasks directly in any column without opening a modal - just click the "+" button.

### Keyboard Shortcuts
- `Ctrl/Cmd + K`: Quick add task
- `Esc`: Close modals

### Dark Mode
Persistent dark mode preference saved to localStorage.

### Responsive Design
Fully responsive layout that works on desktop, tablet, and mobile devices.

## 🔒 Security Features

### Backend Security
- **SQL Injection Protection**: Pattern-based detection in query parameters
- **XSS Protection**: Input sanitization and validation
- **Rate Limiting**: 100 requests per 60 seconds per IP address
- **Security Headers**:
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - X-XSS-Protection: 1; mode=block
- **Request Logging**: Complete audit trail of all API requests with IP tracking
- **CORS Configuration**: Controlled cross-origin access

### Frontend Security
- **API Key Storage**: Secure storage in localStorage
- **Input Validation**: Client-side validation before API calls
- **Error Handling**: Graceful error messages without exposing internals

## 📁 Project Structure

```
Mini_Task_Board_Technical_Test/
├── backend/
│   ├── taskboard/              # Django project settings
│   │   ├── settings.py         # Configuration with security settings
│   │   ├── urls.py             # URL routing
│   │   └── wsgi.py
│   ├── tasks/                  # Tasks app
│   │   ├── models.py           # Task model with Status/Priority enums
│   │   ├── views.py            # Enhanced API views with filtering
│   │   ├── serializers.py      # DRF serializers with validation
│   │   ├── middleware.py       # API key authentication
│   │   ├── security_middleware.py  # Security protections
│   │   ├── admin.py            # Enhanced admin panel
│   │   ├── test_models.py      # 25 model tests
│   │   ├── test_views.py       # 35 view tests
│   │   ├── test_serializers.py # 23 serializer tests
│   │   ├── test_middleware.py  # 11 middleware tests
│   │   └── urls.py
│   ├── logs/                   # Application logs
│   │   ├── django.log
│   │   └── security.log
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Button.jsx
│   │   │   ├── Button.test.jsx
│   │   │   ├── TaskCard.jsx
│   │   │   ├── TaskForm.jsx
│   │   │   ├── Toast.jsx
│   │   │   ├── QuickAddTask.jsx
│   │   │   └── ...
│   │   ├── contexts/           # React contexts
│   │   │   ├── AuthContext.jsx
│   │   │   └── AuthContext.test.jsx
│   │   ├── pages/              # Page components
│   │   │   ├── Login.jsx
│   │   │   └── Board.jsx
│   │   ├── services/           # API services
│   │   │   ├── api.js
│   │   │   └── api.test.js
│   │   ├── test/               # Test setup
│   │   │   └── setup.js
│   │   └── main.jsx
│   ├── coverage/               # Test coverage reports
│   ├── package.json
│   ├── vite.config.js
│   ├── vitest.config.js
│   └── tailwind.config.js
└── README.md
```

## 🛠️ Admin Panel

Access the enhanced Django admin panel at `http://127.0.0.1:8000/admin`

Features:
- Color-coded status and priority badges
- Bulk actions for changing status/priority
- Advanced filtering options
- Task statistics display
- Task age calculation ("Today", "2 days ago", etc.)
- Date hierarchy navigation

## 🐛 Troubleshooting

### Port Already in Use

**Backend:**
```bash
# Find and kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

**Frontend:**
Vite will automatically try ports 5173, 5174, 5175. Update CORS settings in `backend/taskboard/settings.py` if needed.

### API Key Issues

Make sure the API key in frontend matches the backend:
- Frontend: Check `.env` file or localStorage
- Backend: Check `backend/taskboard/settings.py` → `API_KEY` variable

### Database Issues

Reset the database:
```bash
cd backend
rm db.sqlite3
python manage.py migrate
```

## 📈 Performance Optimizations

- **Optimistic UI Updates**: Instant feedback for drag-and-drop and status changes
- **Pagination**: Efficient data loading with configurable page sizes
- **Lazy Loading**: Components loaded on demand
- **Debounced Search**: Reduces API calls during search
- **Memoization**: React components optimized with proper key usage

## 🚀 Deployment

### Backend (Django)

For production deployment:
1. Set `DEBUG=False` in settings
2. Use PostgreSQL instead of SQLite
3. Configure proper `SECRET_KEY`
4. Set up static files serving
5. Use Gunicorn or uWSGI as WSGI server
6. Set up HTTPS with proper security headers

### Frontend (React)

```bash
cd frontend
npm run build
```

Deploy the `dist/` folder to:
- Netlify
- Vercel
- AWS S3 + CloudFront
- Any static hosting service

## 📝 Features Checklist

### Required Features ✅
- ✅ Authentication (API key with middleware)
- ✅ Login screen with validation
- ✅ Logged-in state persists
- ✅ Task board with three columns
- ✅ Create/Edit/Delete tasks
- ✅ Drag and drop between columns
- ✅ Search by title
- ✅ Filter by priority
- ✅ Loading states
- ✅ Empty states
- ✅ Form validation
- ✅ Responsive layout
- ✅ Visual polish

### Bonus Features ✅
- ✅ Dark mode toggle
- ✅ Keyboard accessibility (ESC, Ctrl+K, focus management)
- ✅ Optimistic UI updates
- ✅ Smooth animations
- ✅ Toast notifications
- ✅ Quick add tasks
- ✅ Enhanced security middleware

### Testing ✅
- ✅ 94 backend tests (95% coverage)
- ✅ 38 frontend tests (78% coverage)
- ✅ All tests passing

## 🎓 Technical Highlights

### Architecture Decisions
- **API Key Authentication**: Chose simplicity over JWT for faster development
- **React Context API**: Sufficient for small-to-medium state management
- **Optimistic Updates**: Improves perceived performance
- **Security-First**: Multiple layers of protection (SQL injection, XSS, rate limiting)

### Code Quality
- **DRY Principle**: Reusable components and utilities
- **Separation of Concerns**: Clean architecture with contexts, services, and components
- **Type Safety**: PropTypes for React components
- **Error Handling**: Comprehensive try-catch blocks and user-friendly messages

### Testing Strategy
- **Unit Tests**: Individual components and functions
- **Integration Tests**: API endpoints with authentication
- **Security Tests**: Middleware and protection mechanisms
- **Coverage Reports**: HTML reports for detailed analysis

## 📝 License

This project is created for educational and demonstration purposes.

## 👤 Author

**Halima Ben Chaa**
- GitHub: [@halimabenchaapro-pixel](https://github.com/halimabenchaapro-pixel)

## 🙏 Acknowledgments

- Django REST Framework documentation
- React documentation
- Tailwind CSS team
- Testing Library community

---

**Note**: This is a technical test project demonstrating full-stack development capabilities with modern best practices, comprehensive testing (95% backend, 78% frontend), and enterprise-level security measures.

**Built with ❤️ using Django REST Framework and React**
