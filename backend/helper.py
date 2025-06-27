from database_conn import db

def save_to_db(data):
    db.session.add(data)
    db.session.commit()