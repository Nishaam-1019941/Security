from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Teacher(UserMixin, db.Model):
    __tablename__ = 'teachers'
    teacher_id = db.Column(db.Integer, primary_key=True)
    display_name= db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    teacher_password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.teacher_id)
    
    def id(self):
        return self.teacher_id


    def is_active(self):
        return True  


class Note(db.Model):
    __tablename__ = 'notes'
    note_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=True)
    note_source = db.Column(db.String(255))
    is_public = db.Column(db.String(3))
    teacher_id = db.Column(db.Integer) 
    category_id = db.Column(db.Integer) 
    note = db.Column(db.Text)

class Question(db.Model):
    __tablename__ = 'questions'
    questions_id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, db.ForeignKey('notes.note_id'), nullable=False)
    exam_question = db.Column(db.String(255), nullable=False)
    multiple_choice = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Question questions_id={self.questions_id} note_id={self.note_id} exam_question={self.exam_question} date_created={self.date_created}>"


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    omschrijving = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Category(category_id={self.category_id}, omschrijving={self.omschrijving})"