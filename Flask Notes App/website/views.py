from flask import Blueprint,render_template,request,flash,jsonify
from flask_login import login_required,current_user
from website.models import Note
from website import db
import json

views = Blueprint('views',__name__)

@views.route("/",methods=['GET','POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) == 0:
            flash('Empty notes are not accepted')
        else:
            note = Note(data=note,user_id=current_user.id)
            db.session.add(note)
            db.session.commit()
            flash('Note added','success')
    return render_template('home.html',title='Home')

@views.route("/delete-note",methods=['POST'])
def delete_note():
        note = json.loads(request.data)
        noteId= note['noteId']
        note = Note.query.get(noteId)
        if note:
            if note.user_id == current_user.id:
                db.session.delete(note)
                db.session.commit()