from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user,login_required, logout_user, current_user
from .models import Note, User
from . import db, oa
import json


views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) <1:
            flash('Note is too short', category='error')
        else:
            try:
                completion = oa.ChatCompletion.create(
                model="gpt-3.5-turbo",
                max_tokens = 100,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f'I want you save this as note and give the key points of it in 50 words: {note}'}

                ]
                )
                new_note = Note(data=note, gpt=completion.choices[0].message.content, user_id=current_user.id)
                db.session.add(new_note)
                db.session.commit()

            except:
                flash("Check your network and try again.", category='error')
                print("Some errors with the api")

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    data = json.loads(request.data)
    print(f'data : {data}')
    noteId = data['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


