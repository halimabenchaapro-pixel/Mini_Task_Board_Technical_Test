# Mini Task Board

A full-stack task management application built with Django REST Framework and React with Tailwind CSS.

## Features

### Core Functionality
- **Task CRUD Operations**: Create, read, update, and delete tasks
- **Task Board with Three Columns**: Backlog, In Progress, and Done
- **Drag and Drop**: Move tasks between columns with smooth animations
- **Search and Filter**: Client-side search by title and filter by priority
- **API Key Authentication**: Simple X-API-KEY header authentication
- **Form Validation**: Comprehensive validation with error messages
- **Responsive Design**: Mobile-friendly layout

### Task Fields
- Title (required)
- Description (optional)
- Status (Backlog, In Progress, Done)
- Priority (Low, Medium, High)
- Due Date (optional)
- Created At (auto-generated)

### UX Features
- Loading states with spinners
- Empty states for each column
- Form validation messages
- Responsive layout (mobile friendly)
- Visual polish: spacing, typography hierarchy, buttons, hover states

### Bonus Features Implemented
- **Dark Mode**: Toggle between light and dark themes with persistent preference
- **Keyboard Accessibility**: ESC key to close modals, focus management
- **Optimistic UI Updates**: Immediate UI feedback for drag-and-drop operations
- **Animations**: Subtle transitions and animations throughout the app

## Tech Stack

### Backend
- **Django 4.2.9**: Web framework
- **Django REST Framework 3.14.0**: API framework
- **django-cors-headers 4.3.1**: CORS support
- **python-dotenv 1.0.0**: Environment variable management
- **SQLite**: Database (default Django database)

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **React Router DOM**: Client-side routing
- **Axios**: HTTP client
- **@hello-pangea/dnd**: Drag and drop functionality

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Setup Instructions

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   ```bash
   cp .env.example .env
   # Edit .env and set your API key if needed
   ```

5. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (optional, for Django admin):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

   The API will be available at `http://localhost:8000/api/`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # The default values should work for local development
   ```

4. **Start the development server**:
   ```bash
   npm run dev
   ```

   The application will be available at `http://localhost:5173/` (or the next available port)

## Environment Variables

### Backend (.env)
```
SECRET_KEY=your-secret-key-here
DEBUG=True
API_KEY=dev-api-key-12345
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000/api
VITE_API_KEY=dev-api-key-12345
```

**Note**: The default API key for development is `dev-api-key-12345`. Use this when logging in.

## Running Tests

### Backend Tests

```bash
cd backend
source venv/bin/activate
python manage.py test
```

Tests cover:
- Task creation with validation
- Task status updates
- Task deletion
- API key authentication
- Error handling

## API Endpoints

All endpoints require the `X-API-KEY` header with a valid API key.

### Tasks
- `GET /api/tasks/` - List all tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/:id/` - Retrieve a specific task
- `PUT/PATCH /api/tasks/:id/` - Update a task
- `DELETE /api/tasks/:id/` - Delete a task

### Example Request
```bash
curl -X GET http://localhost:8000/api/tasks/ \
  -H "X-API-KEY: dev-api-key-12345"
```

## Project Structure

```
mini-task-board/
├── backend/
│   ├── taskboard/          # Django project settings
│   ├── tasks/              # Tasks app
│   │   ├── models.py       # Task model
│   │   ├── serializers.py  # DRF serializers
│   │   ├── views.py        # API views
│   │   ├── urls.py         # API URLs
│   │   ├── middleware.py   # API key authentication
│   │   └── tests.py        # Backend tests
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable components
│   │   ├── contexts/       # React contexts (Auth, Theme)
│   │   ├── pages/          # Page components (Login, Board)
│   │   ├── services/       # API service
│   │   └── utils/          # Utility functions
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## Technical Decisions

### Authentication Approach
I chose **API key authentication** (Option A from the requirements) for simplicity and faster implementation. This approach:
- Reduces complexity by avoiding user management
- Is suitable for the project's scope and timeframe
- Uses Django middleware for clean request interception
- Validates the API key on every request to protected endpoints

### State Management
I used **React Context API** for state management because:
- The app has minimal global state (auth and theme)
- Context API is built-in and requires no additional dependencies
- Perfect for this small-to-medium sized application
- Easy to understand and maintain

### Drag and Drop Library
I chose **@hello-pangea/dnd** (maintained fork of react-beautiful-dnd) because:
- Provides excellent accessibility out of the box
- Smooth animations and transitions
- Well-documented API
- Actively maintained

### UI Framework
I used **Tailwind CSS** because:
- Rapid development with utility classes
- Built-in dark mode support
- Excellent responsive design utilities
- Consistent design system
- Small production bundle size

### Optimistic Updates
I implemented optimistic UI updates for drag-and-drop to provide immediate feedback:
- UI updates instantly when dragging tasks
- Rolls back if the API call fails
- Provides better user experience

### Dark Mode Implementation
- Used Tailwind's dark mode with class strategy
- Persists preference in localStorage
- Smooth transitions between themes
- Applied consistently across all components

## Features Checklist

### Required Features
- ✅ Authentication (API key with middleware)
- ✅ Login screen with validation and error display
- ✅ Logged-in state persists (localStorage)
- ✅ Task board UI with three columns
- ✅ Create task (modal)
- ✅ Edit task (same modal)
- ✅ Delete task (with confirmation)
- ✅ Move task between columns (drag and drop)
- ✅ Search tasks by title
- ✅ Filter by priority
- ✅ Loading states (spinner)
- ✅ Empty state per column
- ✅ Form validation messages
- ✅ Responsive layout
- ✅ Visual polish

### API Requirements
- ✅ GET /api/tasks/ (list)
- ✅ POST /api/tasks/ (create)
- ✅ GET /api/tasks/:id/ (detail)
- ✅ PUT/PATCH /api/tasks/:id/ (update)
- ✅ DELETE /api/tasks/:id/ (delete)
- ✅ Validate required fields
- ✅ Enum-like status and priority
- ✅ Meaningful error responses

### Testing
- ✅ Backend: Create task validation test
- ✅ Backend: Update task status test
- ✅ Backend: Delete task test
- ✅ Backend: Authentication tests
- ✅ All tests passing

### Bonus Features (3 implemented)
- ✅ Optimistic UI updates
- ✅ Keyboard accessibility (ESC to close, focus trap)
- ✅ Dark mode toggle
- ✅ Animations (subtle transitions)

## Future Improvements

Given more time, I would consider:
- Server-side pagination and filtering
- User authentication with JWT
- Task assignment and collaboration features
- Task categories/tags
- Docker Compose setup
- CI/CD pipeline
- End-to-end tests with Cypress
- Task audit log
- File attachments
- Task comments

## License

This project was created as a technical assessment.

---

**Built with ❤️ using Django REST Framework and React**
