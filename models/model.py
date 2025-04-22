from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, DateTime, Date, Text, ForeignKey, desc
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import bcrypt

db = SQLAlchemy()

'''=================================================== Admin Model ======================================================'''

class Admin(db.Model):
    __tablename__ = "admin"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8'))


'''=================================================== User Model ======================================================'''

class User(db.Model):
    __tablename__ = "users"  

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(250), nullable=False)
    qualification: Mapped[str] = mapped_column(String(100), nullable=False)
    dob: Mapped[datetime] = mapped_column(Date, nullable=False)

    scores = relationship("Score", backref="user", cascade="all, delete", lazy=True)
    responses = relationship("Response", backref="user", cascade="all, delete", lazy=True)

    def __init__(self, name, email, password, qualification, dob):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        self.qualification = qualification
        self.dob = datetime.strptime(dob, "%Y-%m-%d").date()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('UTF-8'), self.password.encode('UTF-8'))


'''=================================================== Subject Model ======================================================'''

class Subject(db.Model):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    desc: Mapped[str] = mapped_column(Text, nullable=False)

    chapters = relationship("Chapter", backref="subject", cascade="all, delete", lazy=True)


'''=================================================== Chapter Model ======================================================'''

class Chapter(db.Model):
    __tablename__ = "chapters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    desc: Mapped[str] = mapped_column(Text)
    subjectId: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)

    quizzes = relationship("Quiz", backref="chapter", cascade="all, delete", lazy=True)


'''=================================================== Quiz Model ======================================================'''

class Quiz(db.Model):
    __tablename__ = "quizzes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration: Mapped[int] = mapped_column(nullable=False)
    desc: Mapped[str] = mapped_column(Text)
    chapterId: Mapped[int] = mapped_column(ForeignKey("chapters.id"), nullable=False)

    questions = relationship("Question", backref="quiz", cascade="all, delete", lazy=True)
    scores = relationship("Score", backref="quiz", cascade="all, delete", lazy=True)  
    responses = relationship("Response", backref="quiz", cascade="all, delete", lazy=True)  


'''=================================================== Question Model ======================================================'''

class Question(db.Model):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    statement: Mapped[str] = mapped_column(Text, nullable=False)
    option1: Mapped[str] = mapped_column(Text, nullable=False)
    option2: Mapped[str] = mapped_column(Text, nullable=False)
    option3: Mapped[str] = mapped_column(Text, nullable=False)
    option4: Mapped[str] = mapped_column(Text, nullable=False)
    correctOption: Mapped[int] = mapped_column(Integer, nullable=False)
    quizId: Mapped[int] = mapped_column(ForeignKey("quizzes.id"), nullable=False)

    responses = relationship("Response", backref="question", cascade="all, delete", lazy=True)  


'''====================================================== Score Model ======================================================'''

class Score(db.Model):
    __tablename__ = "scores"

    id: Mapped[int] = mapped_column(primary_key=True)
    totalScore: Mapped[int] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=db.func.current_timestamp())
    quizId: Mapped[int] = mapped_column(ForeignKey("quizzes.id"), nullable=False)
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

'''====================================================== Response Model ======================================================'''

class Response(db.Model):
    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(primary_key=True)
    selectedOption: Mapped[int] = mapped_column(nullable=False)
    score: Mapped[int] = mapped_column(nullable=False)
    questionId: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    quizId: Mapped[int] = mapped_column(ForeignKey("quizzes.id"), nullable=False)
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
