from flask import Blueprint, abort, redirect, render_template, request, flash, jsonify, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Note
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", user=current_user)

@views.route('/study-tools')
def studytools():
    return render_template("study-tools.html", user=current_user)

@views.route('/coming-soon')
def comingsoon():
    return render_template("coming-soon.html", user=current_user)

# route for notes (includes add, edit, delete and view notes)
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


@views.route('/search', methods=['GET'])
def search():
    query = request.args.get('s')  # get the search query from the URL parameter
    results = []

    if query and current_user.is_authenticated:
        # search for notes containing the query
        results = Note.query.filter(
            (Note.title.ilike(f"%{query}%")) | (Note.note_data.ilike(f"%{query}%"))
        ).filter_by(user_id=current_user.id).all()
    
    elif not current_user.is_authenticated:
        flash('You need to be logged in to search notes', category='error')
        return redirect(url_for('auth.login'))

    return render_template('search.html', query=query, results=results, user=current_user)