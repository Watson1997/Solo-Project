from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app.models import user

class Song():
    def __init__(self, data):
        self.id = data['id']
        self.artist = data['artist']
        self.song = data['song']
        self.date_recorded = data['date_recorded']
        self.created_at = data ['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

        self.creator = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM songs"
        results = connectToMySQL('MusiciansCab').query_db(query)
        all_songs = []
        for row in results:
            all_songs.append(cls(row))
        return all_songs

    @staticmethod
    def song_validator(data):
        is_valid = True
        if len(data['artist']) < 3:
            flash("Artist must be 3 characters.", "create")
            is_valid=False
        if len(data['song']) < 3:
            flash("Song must be 3 characters.", "create")
            is_valid=False

        return is_valid

    @classmethod
    def create_song(cls, form_data):
        query = "INSERT INTO songs (artist, song, date_recorded, users_id) VALUES (%(artist)s, %(song)s, %(date_recorded)s, %(users_id)s)"
        return connectToMySQL('MusiciansCab').query_db(query, form_data)

    @classmethod
    def get_all_songs_with_users(cls):
        query = "SELECT * FROM songs LEFT JOIN users ON songs.users_id = users.id;"
        songs = connectToMySQL('MusiciansCab').query_db(query)
        results = []
        for song in songs:
            user_data = {
                'id' : song['users.id'],
                'first_name' : song['first_name'],
                'last_name' : song['last_name'],
                'email' : song['email'],
                'password' : song['password'],
                'created_at' : song['users.created_at'],
                'updated_at' : song['users.updated_at']
            }
            one_song = cls(song)
            one_song.creator = user.User(user_data)
            results.append(one_song)
        return results


    @classmethod 
    def get_one(cls, data):
        query = "SELECT * FROM songs WHERE id = %(id)s"
        results = connectToMySQL('MusiciansCab').query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls, form_data):
        query = "UPDATE songs SET artist = %(artist)s, song = %(song)s, date_recorded = %(date_recorded)s WHERE id = %(id)s"
        return connectToMySQL('MusiciansCab').query_db(query, form_data)

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM songs WHERE id = %(id)s"
        return connectToMySQL('MusiciansCab').query_db(query, data)


