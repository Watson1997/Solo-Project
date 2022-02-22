from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.song import Song
from flask_app.models.user import User


@app.route('/new/song')
def new_song():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_song.html',user=User.get_by_id(data))


@app.route('/create/song',methods=['POST'])
def create_song():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Song.song_validator(request.form):
        return redirect('/new/song')
    data = {
        "artist": request.form["artist"],
        "song": request.form["song"],
        "date_recorded": request.form["date_recorded"],
        "users_id": session["user_id"]
    }
    Song.create_song(data)
    return redirect('/dashboard')

@app.route('/edit/song/<int:id>')
def edit_song(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_song.html",edit=Song.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/song/<int:id>',methods=['POST'])
def update_song(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Song.song_validator(request.form):
        return redirect('/new/song')
    data = {
        "artist": request.form["artist"],
        "song": request.form["song"],
        "date_recorded": request.form["date_recorded"],
        "id" :  id 
    }
    Song.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show.html",show=Song.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/song/<int:id>')
def destroy_show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Song.destroy(data)
    return redirect('/dashboard')

