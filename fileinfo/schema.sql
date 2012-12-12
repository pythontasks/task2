drop table if exists files;
create table w(
	id integer primary key autoincrement,
	path string not null,
	mode integer,
	ino integer,
	dev string,
	nlink integer,
	uid integer,
	gid integer,
	size integer,
	atime string,
	mtime string,
	ctime string,
	need_update integer
	);