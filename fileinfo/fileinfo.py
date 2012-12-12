from contextlib import closing
from tasks import infofiles, scandirs
import sqlite3
from celery import Celery
from flask import Flask, g, jsonify
from datetime import timedelta

celery = Celery('tasks', broker='redis://localhost')

#configuration
DATABASE = 'fileinfo.sqlite3'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

if __name__ == '__main__':
    app.run()
    scandirs.delay()

	celery.conf.CELERYBEAT_SCHEDULE = {
    'runs-every-minute: {
        'task': 'tasks.infofiles',
        'schedule': timedelta(seconds=60),
    },
}

def init_db():
    with closing(connect_db()) as db:
    	with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def listfiles():
	cur = g.db.execute('SELECT id, path FROM files')
	files = [{'id':row[0], 'files':row[1]}  for row in cur.fetchall()] 
	return jsonify(result = files)

@app.route('/details/<int:file_id>')
def filedetails(file_id):
	cur = g.db.execute('SELECT * FROM files WHERE id=%d', (file_id,)) #* includes all columns form shcema.sql
	file_1 = cur.fetchone()
	return jsonify(result = file_1)



