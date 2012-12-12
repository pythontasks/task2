from celery import Celery
import os
import time
from fileinfo import connect_db

celery = Celery('tasks', broker='redis://localhost')

@celery.task
def scandirs():
	db = connect_db()
	for root, dirs, files in os.walk('/'):
		files2 = [os.path.join(root, f) for f in files]
	
		for f2 in files2:
			db.execute('INSERT INTO files (path, need_update)
				VALUES (%s, 1)', (f2,))
	db.close()

@celery.task 
def infofiles():
	db = connect_db()
	cur= db.execute('SELECT path FROM files WHERE need_update = 1')
	for index in range(cur.rowcount):
		path = cur.fetchone()[0]
		filestat = os.stat(path)
		db.execute('UPDATE files SET  mode = %i,ino = %i,dev = %s,nlink = %i, uid = %i,gid = %i,size = %i,atime = %s,mtime = %s,ctime = %s, need_update = 0 WHERE path = %s', (filestat.st_mode, filestat.st_ino, filestat.st_dev, filestat.st_nlink, filestat.st_uid, filestat.st_gid, filestat.st_size, time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(filestat.st_atime)), time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(filestat.st_mtime)), time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(filestat.st_ctime)), path) )
	db.close()