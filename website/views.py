from flask import Blueprint, abort, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Note, Flashcard
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/study-tools')
def studytools():
    return render_template("study-tools.html", user=current_user)


@views.route('/study-tools/notes/<int:note_id>', methods=['GET', 'POST'])
@login_required
def show_notes(note_id):
    note = Note.query.get(note_id)

    if not note:    
        flash('Note not found', category='error')
        return redirect(url_for('views.studytools'))  # this will redirect to notes list
    
    if note.user_id != current_user.id:
        flash('You do not have permission to view this note', category='error')
        return redirect(url_for('views.studytools'))

    notes_list = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("study-tools.html", notes=notes_list, current_note=note, user=current_user)


@views.route('study-tools/notes/new', methods=['GET', 'POST'])
@login_required
def add_note():
    if request.method == "POST":
        note = request.form.get('note')
        title = request.form.get('title')

        if not note:
            flash('..It\'s empty?', category='error')

        elif not title:
            flash('Please add a title to your note.', category='error')

        else:
            new_note = Note(note_data=note, title=title, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note saved!', category='success')
            return redirect(url_for('views.studytools'))

    return render_template("add-note.html", user=current_user)


@views.route('study-tools/notes/edit/<int:note_id>', methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get(note_id)

    if not note:
        flash('Note not found', category='error')
        return redirect(url_for('views.studytools'))  # this will redirect to notes list
    
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note', category='error')
        return redirect(url_for('views.studytools'))

    if request.method == "POST":
        edit_note = request.form.get('note')
        edit_title = request.form.get('title')

        if not edit_note or not edit_title:
            if not note:
                flash('..It\'s empty?', category='error')  #this will return to the edit mode for the note if input is empty 

            if not edit_title:
                flash('Please add a title to your note.', category='error')
            
            return render_template("edit-note.html", user=current_user, notes=Note.query.filter_by(user_id=current_user.id).all(), current_note=note)

        else:
            note.note_data = edit_note
            note.title = edit_title
            db.session.commit()
            flash('Changes saved successfully!', category='success')
            return redirect(url_for('views.show_notes', note_id=note_id))     #if saved successfully, it will show the note
    

    notes_list = Note.query.filter_by(user_id=current_user.id).all()
    return render_template("edit-note.html", user=current_user, notes=notes_list, current_note=note)     #this will render the edit_note.html and it will pass those variables to that html


@views.route('study-tools/notes/delete/<int:note_id>', methods=['GET'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    db.session.delete(note)
    db.session.commit()
    flash('Note Deleted!', category='success')
    return redirect(url_for('views.studytools'))


@views.route('/flashcards', methods=['GET'])
def flashcards():
    flashcards = Flashcard.query.all()
    return render_template('flashcards.html', flashcards=flashcards, user=current_user)

@views.route('/flashcards', methods=['POST'])
def add_flashcard():
    if request.method == "POST":
        question = request.form.get('question')
        answer = request.form.get('answer')

        new_flashcard = Flashcard(question=question, answer=answer, user_id=current_user.id)
        db.session.add(new_flashcard)
        db.session.commit()
        flash('Flashcard saved!', category='success')
        return redirect(url_for('views.flashcards'))
    
    return render_template("flashcards.html", user=current_user)

@views.route('/flashcards/edit/<int:id>', methods=['GET', 'POST'])
def update_flashcard(id):
    flashcard = Flashcard.query.get_or_404(id)

    if not flashcard:
        flash('Note not found', category='error')
        return redirect(url_for('views.flashcards'))
    
    if flashcard.user_id != current_user.id:
        flash('You do not have permission to edit this note', category='error')
        return redirect(url_for('views.flashcards'))
    
    if request.method == "POST":
        edit_fc_answer = request.form.get('answer')
        edit_fc_question = request.form.get('question')

        flashcard.answer = edit_fc_answer
        flashcard.question = edit_fc_question
        db.session.commit()
        flash('Changes saved successfully!', category='success')
        return redirect(url_for('views.flashcards'))
    
    return render_template("flashcards.html", user=current_user)
    
    
    # flashcard.question = request.json['question']
    # flashcard.answer = request.json['answer']
    # db.session.commit()
    # return jsonify({"message": "Flashcard updated successfully"})


# Route to delete a flashcard
@views.route('/flashcards/delete/<int:id>', methods=['GET'])
def delete_flashcard(id):
    flashcard = Flashcard.query.get_or_404(id)
    db.session.delete(flashcard)
    db.session.commit()
    flash('Flashcard Deleted!', category='success')
    return redirect(url_for('views.flashcards'))


@views.route('/calendar')
def calendar():
    return render_template("calendar.html", user=current_user)


@views.route('/view', methods=['GET'])
def view_content():
    notes = Note.query.all()
    return render_template('view_notes.html', notes=notes, user=current_user)

@views.route('/save', methods=['POST'])
def save_content():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('editor_content')

        if not content:
            flash('..It\'s empty?', category='error')

        elif not title:
            flash('Please add a title to your note.', category='error')

        else:
            note = Note(title=title, note_data=content, user_id=current_user.id)
            db.session.add(note)
            db.session.commit()
            return redirect(url_for('views.view_content'))