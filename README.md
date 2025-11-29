# Django Quiz & Events Application

A web application built with Django that allows users to take interactive quizzes and view upcoming events.

## Features

### Quiz Section
- Browse all available quizzes
- View quiz details before starting
- Dynamic quiz attempt page with questions and multiple choice answers
- Support for single and multiple choice questions
- Automatic score calculation
- Detailed results page showing correct/incorrect answers
- User submission tracking

### Events Section
- Display upcoming events with date, time, and location
- Show past events separately
- Clean, organized event listing

### Frontend
- Responsive design using Tailwind CSS
- Modern, clean UI with gradient backgrounds
- Interactive components with hover effects
- Mobile-friendly layout

## Technology Stack

- **Backend**: Django 5.x
- **Database**: SQLite
- **Frontend**: HTML + Tailwind CSS (via CDN)
- **Optional**: Django REST Framework

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd django_quiz_events
   ```

2. **Create and activate virtual environment**
   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Load sample data (optional)**
   ```bash
   python manage.py loaddata sample_data.json
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
django_quiz_events/
│
├── quiz_events_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── quiz_app/
│   ├── migrations/
│   ├── templates/
│   │   └── quiz_app/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── quiz_list.html
│   │       ├── quiz_detail.html
│   │       ├── quiz_attempt.html
│   │       ├── quiz_result.html
│   │       └── event_list.html
│   ├── fixtures/
│   │   └── sample_data.json
│   ├── admin.py
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── manage.py
├── requirements.txt
└── README.md
```

## Models

### Quiz
- `title`: Quiz title
- `description`: Quiz description
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Question
- `quiz`: Foreign key to Quiz
- `text`: Question text
- `question_type`: Single or multiple choice
- `created_at`: Creation timestamp

### Answer
- `question`: Foreign key to Question
- `text`: Answer text
- `is_correct`: Boolean flag for correct answer

### UserSubmission
- `quiz`: Foreign key to Quiz
- `user_name`: Name of the user
- `score`: Total score achieved
- `submitted_at`: Submission timestamp

### UserAnswer
- `submission`: Foreign key to UserSubmission
- `question`: Foreign key to Question
- `answer`: Foreign key to Answer
- `is_correct`: Boolean flag for correct answer

### Event
- `title`: Event title
- `description`: Event description
- `date`: Event date and time
- `location`: Event location

## Usage

### Admin Panel

1. Login to admin panel at `/admin/`
2. Add quizzes with questions and answers
3. Mark correct answers for each question
4. Add events with dates and locations

### Taking a Quiz

1. Browse available quizzes on the home page or quiz list page
2. Click "Start Quiz" to view quiz details
3. Click "Start Quiz Now" to begin
4. Enter your name
5. Answer all questions
6. Submit the quiz
7. View your results with detailed feedback

### Viewing Events

1. Navigate to the Events page
2. View upcoming events with dates and locations
3. Past events are shown separately

## Sample Data

The project includes sample data with:
- 2 quizzes (Python Basics, Django Framework)
- Multiple questions per quiz
- 3 sample events

Load it using:
```bash
python manage.py loaddata sample_data.json
```

## API Endpoints (Optional - if using DRF)

The project is ready for REST API implementation. To add API endpoints:

1. Uncomment `rest_framework` in `INSTALLED_APPS`
2. Create serializers in `quiz_app/serializers.py`
3. Create API views in `quiz_app/api_views.py`
4. Add API URLs in `quiz_app/urls.py`

## Development

### Adding New Features

1. **Add new models**: Update `models.py` and run migrations
2. **Add new views**: Create views in `views.py`
3. **Add new templates**: Create HTML files in `templates/quiz_app/`
4. **Add new URLs**: Update `urls.py`

### Running Tests

```bash
python manage.py test
```

## Deployment Considerations

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Set up static files with `python manage.py collectstatic`
5. Use a production-ready web server (Gunicorn, uWSGI)
6. Set up environment variables for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is created for interview purposes.

## Support

For issues or questions, please create an issue in the repository.

---

**Built with Django + Tailwind CSS**
