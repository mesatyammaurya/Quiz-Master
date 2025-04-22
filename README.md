## Quiz Master

## Project Description
Quiz Master is a web-based platform designed to manage quizzes efficiently. The system allows users to register, take quizzes, and track their scores, while administrators can create and manage quizzes and users. The primary goal is to create an interactive and user-friendly quiz system with a structured backend.

---

## Technologies Used
- **Python**: The core programming language for implementing logic, handling data, and managing routes.
- **Flask (Web Framework)**: A lightweight and flexible framework for building web applications.
- **Flask-SQLAlchemy (ORM)**: Manages databases using Python objects instead of raw SQL queries.
- **Flask-Bcrypt (Password Hashing)**: Ensures secure password storage through hashing.
- **Flask-WTF**: Facilitates form handling and validation.
- **SQLite / MySQL**: Efficiently stores and manages quiz-related data.
- **Jinja2 (Templating Engine)**: Dynamically renders HTML templates.
- **HTML5, CSS & JavaScript**: Provides structure, styling, and interactivity for the frontend.
- **Bootstrap 5 (CSS Framework)**: Ensures a responsive and visually appealing UI.
- **Git & GitHub**: Enables version control, collaboration, and project tracking.

---

## **Project Architecture**
```
quiz-master/
│── app.py              # Main entry point of the application
│
├── controllers/        # Handles core application logic and API requests
│   ├── routes.py       # Defines API endpoints
│   ├── appFunctions.py # Helper functions for quiz operations
│   ├── forms.py        # Manages form validation
│
├── models/             # Contains database schema and ORM models
│   ├── model.py        # Defines SQLAlchemy models
│   ├── __init__.py     # Initializes database connection
│
├── instance/
│   ├── database.db     # SQLite database storing quiz-related data
│
├── migrations/         # Database version control and schema migrations
│
├── static/             # Frontend assets (CSS, JS, images)
│   ├── script.js       # Client-side interactions
│   ├── styles.css      # Styling for web pages
│   ├── images/         # Static images used in the app
│
├── templates/          # HTML templates for dynamic page rendering
│
├── quizenv/            # Virtual environment containing dependencies
│
├── .gitignore          # Specifies files to be ignored by Git
├── README.md           # Project documentation
├── requirements.txt    # Lists required dependencies
└── config.py           # Application configurations
```

---

## **Features Implemented**
- **User Authentication**: Secure login and registration with password hashing.
- **Quiz Management**: Admins can create, edit, and delete quizzes.
- **Question Handling**: Supports multiple-choice and descriptive questions.
- **Real-time Scoring**: Automatically evaluates user responses and records scores.
- **Performance Tracking**: Users can review past quiz attempts.
- **Admin Dashboard**: Enables quiz and user management.
- **Bootstrap UI**: Ensures a responsive and visually appealing interface.
- **Database Storage**: Uses SQLite for efficient and lightweight data management.
- **Role-based Access Control**: Differentiates between user and admin functionalities.

---

## **DB Schema Design**
- **Users Table**: Stores user details (ID, Name, Email, Password, Role).
- **Subjects Table**: Manages different quiz topics.
- **Chapters Table**: Divides subjects into specific areas.
- **Quizzes Table**: Contains metadata of quizzes (ID, Name, Subject_ID, Chapter_ID).
- **Questions Table**: Stores quiz questions with possible answers.
- **Responses Table**: Tracks user responses and correctness.
- **Scores Table**: Maintains quiz scores and user progress.

---

## **Installation & Setup**
1. **Clone the repository**
   ```sh
   git clone https://github.com/your-username/quiz-master.git
   cd quiz-master
   ```

2. **Set up a virtual environment**
   ```sh
   python -m venv quizenv
   source quizenv/bin/activate  # On Windows, use 'quizenv\Scripts\activate'
   ```

3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```sh
   flask db init
   flask db migrate -m "Initial migration."
   flask db upgrade
   ```

5. **Start the application**
   ```sh
   python app.py
   ```

6. **Open the browser and navigate to**
   ```
   http://127.0.0.1:5000/
   ```

---

