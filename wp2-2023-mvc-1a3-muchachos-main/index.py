from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from classes import db, Teacher, Note, Question, Category
from vragen import TestGPT

from flask_paginate import Pagination, get_page_args
from sqlalchemy import or_

import os
import csv
import io


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'databases', 'testgpt.db')
app.config['SECRET_KEY'] = 'test'

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

api_key = "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"
test_gpt = TestGPT(api_key)


@app.route('/export_csv')
@login_required
def export_csv():
    # Check if the user is an admin or the owner of the notes
    if current_user.is_admin:
        notes = Note.query.all()
    else:
        notes = Note.query.filter_by(teacher_id=current_user.id).all()

    # Prepare the CSV data
    csv_data = [['Title', 'Source', 'Is Public','TeacherID','CategoryID', 'Note', 'Open Question', 'Multiple Choice Question']]

    for note in notes:
        open_question = Question.query.filter_by(note_id=note.note_id, multiple_choice=False).first()
        multiple_choice_question = Question.query.filter_by(note_id=note.note_id, multiple_choice=True).first()

        csv_data.append([
            note.title,
            note.note_source,
            note.is_public,
            note.teacher_id,
            note.category_id,
            note.note,
            open_question.exam_question if open_question else '',
            multiple_choice_question.exam_question if multiple_choice_question else ''
        ])

    # Create a CSV response
    csv_filename = 'exported_notes_with_questions.csv'
    csv_string = io.StringIO()
    csv_writer = csv.writer(csv_string)
    csv_writer.writerows(csv_data)

    response = Response(
        csv_string.getvalue(),
        content_type='text/csv'
    )
    response.headers['Content-Disposition'] = f'attachment; filename={csv_filename}'

    return response

@login_manager.user_loader
def load_user(teacher_id):
    return Teacher.query.get(int(teacher_id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        teacher = Teacher.query.filter_by(username=username).first()
            
        if teacher and teacher.teacher_password == password:
            login_user(teacher)
            return redirect(url_for('homepage'))
        else:
            return render_template('index.html', error='Invalid username or password')

    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()  
    return redirect(url_for('login'))

@app.route('/teachers', methods=['GET', 'POST'])
@login_required
def teachers():
    all_teachers = Teacher.query.all()
    if current_user.is_admin:
        if request.method == 'POST':
            display_name = request.form['display_name']
            username = request.form['username']
            teacher_password = request.form['teacher_password']
            is_admin = 'is_admin' in request.form  

            new_teacher = Teacher(
                display_name=display_name,
                username=username,
                teacher_password=teacher_password,
                is_admin=is_admin
            )
            db.session.add(new_teacher)
            db.session.commit()

            return redirect(url_for('teachers'))

        return render_template('teachers.html', teachers=all_teachers)
    else:   
        return 'Access denied. You do not have permission to access this page.'


@app.route('/homepage')
def homepage():
    return render_template('homepage.html')

@app.route('/overzicht')
def overzicht():
    per_page = 20
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    
    if current_user.is_authenticated:
        if current_user.is_admin:
            notes = Note.query.offset(offset).limit(per_page).all()
            total = Note.query.count()
            pagination = Pagination(page=page, per_page=20, total=total, css_framework='bootstrap4')
        else:
            notes = Note.query.filter((Note.teacher_id == current_user.teacher_id) | (Note.is_public == 'JA')).offset(offset).limit(per_page).all()
            total = Note.query.filter((Note.teacher_id == current_user.teacher_id) | (Note.is_public == 'JA')).count()
            pagination = Pagination(page=page, per_page=20, total=total, css_framework='bootstrap4')

        return render_template('overzicht.html', notities=notes, get_category_omschrijving=get_category_omschrijving, pagination=pagination)
    else:
        return redirect(url_for('login'))



@app.route('/maak_notitie', methods=['POST'])
def maak_notitie():
    title = request.form.get('title')
    source = request.form.get('source')
    is_public = 'JA' if 'is_public' in request.form else 'NEE'
    note_content = request.form.get('note')

    teacher_id = current_user.teacher_id
    category_id = 1

    if title is not None:
        nieuwe_notitie = Note(
            title=title,
            note_source=source,
            is_public=is_public,
            teacher_id=teacher_id,
            category_id=category_id,
            note=note_content
        )
        db.session.add(nieuwe_notitie)
        db.session.commit()


        return redirect(url_for('docentenpagina'))
    else:
        return 'Title is required. Please provide a title.'

@app.route('/notes/<int:note_id>')
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    return render_template('view_note.html', note=note)

@app.route('/show_questions/<int:note_id>')
def show_questions(note_id):

    note = Note.query.get(note_id)
    questions = Question.query.filter_by(note_id=note_id).all()

    # Initialize variables
    open_question = None
    multiple_choice_question = None

    # Check if questions already exist for the note
    if not questions:
        # Generate questions only if none exist
        open_question = test_gpt.generate_open_question(note.note)
        multiple_choice_question = test_gpt.generate_multiple_choice_question(note.note)

        if open_question:
            db.session.add(Question(note_id=note_id, exam_question=open_question))
        if multiple_choice_question:
            db.session.add(Question(note_id=note_id, exam_question=multiple_choice_question, multiple_choice=True))

        db.session.commit()

        # Fetch the questions again after committing to the database
        questions = Question.query.filter_by(note_id=note_id).all()

    return render_template('show_questions.html', note=note, questions=questions, open_question=open_question, multiple_choice_question=multiple_choice_question)



@app.route('/edit_note/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)

    if request.method == 'POST':
        note.title = request.form['title']
        note.note_source = request.form['note_source']
        note.note = request.form['note']
        note.is_public = 'JA' if 'is_public' in request.form else 'NEE'

        db.session.commit()

        return redirect(url_for('overzicht', note_id=note.note_id))

    return render_template('edit_note.html', note=note)

@app.route('/delete_note/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get(note_id)

    if note is None:
        flash("Note not found", "error")
        return redirect(url_for('overzicht'))

    # Check if the current user is the owner of the note
    if current_user.is_admin or note.teacher_id == current_user.teacher_id:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted successfully", "success")
    else:
        flash("Access denied. You do not have permission to delete this note.", "error")

    return redirect(url_for('overzicht'))

@app.route('/generate_questions/<int:note_id>', methods=['POST'])
@login_required
def generate_questions(note_id):
    note = Note.query.get(note_id)

    open_question = test_gpt.generate_open_question(note.note)
    multiple_choice_question = test_gpt.generate_multiple_choice_question(note.note)

    if open_question:
        db.session.add(Question(note_id=note_id, exam_question=open_question))
    if multiple_choice_question:
        db.session.add(Question(note_id=note_id, exam_question=multiple_choice_question, multiple_choice=True))

    db.session.commit()

    return redirect(url_for('show_questions', note_id=note_id))


@app.route('/edit_question/<int:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.query.get(question_id)

    if request.method == 'POST':
        new_exam_question = request.form['new_exam_question']

        question.exam_question = new_exam_question
        db.session.commit()

        flash("Question updated successfully", "success")
        return redirect(url_for('show_questions', note_id=question.note_id))

    return render_template('edit_question.html', question=question)


@app.route('/delete_question/<int:question_id>', methods=['GET', 'POST'])
def delete_question(question_id):
    question = Question.query.get(question_id)

    if question is None:
        
        flash("Question not found", "error")
        return redirect(url_for('show_questions', note_id=question.note_id))

    db.session.delete(question)
    db.session.commit()
    flash("Question deleted successfully", "success")

    return redirect(url_for('show_questions', note_id=question.note_id))


@app.route('/docentenpagina', methods=['GET', 'POST'])
def docentenpagina():
    categories = Category.query.all()  
    return render_template('docentenpagina.html', categories=categories)

@app.route('/filter_notes')
def filter_notes():
    search_query = request.args.get('search', '')
    if current_user.is_admin:
        notes = Note.query.filter(Note.title.ilike(f'%{search_query}%') | Note.note.ilike(f'%{search_query}%')).all()
    else:
        notes = Note.query.filter((Note.teacher_id == current_user.teacher_id) | (Note.is_public == 'JA')).filter(Note.title.ilike(f'%{search_query}%') | Note.note.ilike(f'%{search_query}%')).all()

    return render_template('overzicht.html', notities=notes, get_category_omschrijving=get_category_omschrijving)


def get_category_omschrijving(category_id):
    category = Category.query.filter_by(category_id=category_id).first()
    return category.omschrijving if category else 'N/A'

@app.route('/filter_notes_by_category')
def filter_notes_by_category():
    category_filter = request.args.get('category', '')
    
    if current_user.is_admin:
        categories = Category.query.filter(Category.omschrijving.ilike(f'%{category_filter}%')).all()

        if categories:
            
            notes = Note.query.filter((Note.teacher_id == current_user.teacher_id) | (Note.is_public == 'JA')).filter(Note.category_id.in_([category.category_id for category in categories])).all()
        else:
            
            notes = []
    else:
       
        notes = Note.query.filter((Note.teacher_id == current_user.teacher_id) | (Note.is_public == 'JA')).filter(Note.category_id.ilike(f'%{category_filter}%')).all()

    return render_template('overzicht.html', notities=notes, get_category_omschrijving=get_category_omschrijving)



if __name__ == '__main__':
    app.run(debug=True, port=5000)
