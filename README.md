# Best Cars Dealership & Review Application

A full-stack Dealership Application built with **Django REST Framework** and **React JS**, featuring user authentication, car inventory exploration, dealership location filtering, customer reviews management, automated sentiment analysis, and CI/CD deployment pipeline.

---

## Architecture Overview

```
├── server/
│   ├── manage.py
│   ├── requirements.txt
│   ├── package.json
│   ├── djangoproj/             # Django Project Configuration & Middleware
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── djangoapp/              # Django App Backend & REST API
│   │   ├── models.py           # CarMake and CarModel DB Schemas
│   │   ├── views.py            # REST Endpoints (Auth, Dealers, Reviews)
│   │   ├── urls.py             # App Routing
│   │   ├── admin.py            # Django Admin Panel Inline Models
│   │   └── sentiment_analyzer.py # NLTK Sentiment Analysis Engine
│   └── frontend/               # React & Static Frontend Assets
│       ├── src/
│       │   └── components/
│       │       └── Register/
│       │           └── Register.jsx
│       └── static/             # Static HTML Pages & CSS Styling
│           ├── About.html
│           ├── Contact.html
│           └── css/
│               └── style.css
└── .github/
    └── workflows/
        └── django-react-ci.yml # GitHub Actions CI/CD Pipeline
```

---

## Features

1. **User Authentication**: User Registration (5 fields), Login, Logout.
2. **Dealership Directory**: View all dealerships, filter dealerships by State.
3. **Dealer Detail & Reviews**: View individual dealer profiles and real-time user reviews.
4. **Post Review with Sentiment Analysis**: Authenticated users can post reviews; automated sentiment analysis classifies comments as `positive`, `neutral`, or `negative`.
5. **Static Pages**: Modern styled **About Us** and **Contact Us** pages.
6. **Django Admin Panel**: Comprehensive admin interface with `CarModelInline` management.
7. **Automated CI/CD**: Integrated GitHub Actions workflow for building and testing.

---

## REST API Specification

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/djangoapp/register` | Register new user with 5 inputs |
| `POST` | `/djangoapp/login` | Authenticate user credentials |
| `GET`  | `/djangoapp/logout` | Terminate active user session |
| `GET`  | `/djangoapp/get_cars` | List all Car Makes & Car Models |
| `GET`  | `/djangoapp/get_dealers` | Fetch all dealerships |
| `GET`  | `/djangoapp/get_dealers/<state>` | Filter dealerships by State (e.g. TX, MN, AL) |
| `GET`  | `/djangoapp/get_dealer/<id>` | Fetch dealership details by ID |
| `GET`  | `/djangoapp/get_reviews/dealer/<id>` | Retrieve reviews for specific dealership |
| `POST` | `/djangoapp/add_review` | Submit new review with sentiment analysis |
| `GET`  | `/djangoapp/analyze/<text>` | Perform sentiment analysis on arbitrary text |

---

## Setup & Running Instructions

### 1. Backend Setup (Django)

```bash
# Navigate to server directory
cd server

# Install Python dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create Superuser (Admin)
python manage.py createsuperuser

# Start Django Development Server
python manage.py runserver 8000
```

### 2. Accessing the Application

- **Django Admin Panel**: `http://localhost:8000/admin/`
- **About Page**: `http://localhost:8000/about/`
- **Contact Page**: `http://localhost:8000/contact/`
- **REST APIs**: `http://localhost:8000/djangoapp/get_dealers`
