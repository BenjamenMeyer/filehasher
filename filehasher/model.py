from __future__ import print_function
import sqlite3


schemas = [

	[
		'''
		CREATE TABLE IF NOT EXISTS master_files
		(
			hash TEXT NOT NULL PRIMARY KEY,
			path TEXT NOT NULL
		)
		''',
		'''
		CREATE TEMPORARY TABLE IF NOT EXISTS checked_files
		(
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			hash TEXT NOT NULL,
			path TEXT NOT NULL
		)
		'''
	]

]

SQL_INSERT_FILE = '''
	INSERT INTO master_files
	(hash, path)
	VALUES(:hash_value, :path)
'''

SQL_HAS_FILE_BY_HASH = '''
	SELECT hash, path
	FROM master_files
	WHERE hash = :hash_value
'''

SQL_MISSING_FILES = '''
	SELECT hash, path
	FROM master_files
	WHERE hash NOT IN (SELECT hash FROM checked_files)
'''

SQL_CHECK_INSERT_FILE = '''
	INSERT INTO checked_files
	(hash, path)
	VALUES(:hash_value, :path)
'''

SQL_NEW_FILES = '''
	SELECT hash, path
	FROM checked_files
	WHERE hash NOT IN (SELECT hash FROM master_files)
'''


class DataModel(object):

	def __init__(self, datafile):
		self.db = sqlite3.connect(datafile)
		self.init_model()
	
	def init_model(self):
		cursor = self.db.cursor()
		for schema in schemas:
			for table_sql in schema:
				cursor.execute(table_sql)
		self.db.commit()

	def add_file(self, hash_value, path):
		cursor = self.db.cursor()
		args = {
			'hash_value': hash_value,
			'path': path
		}
		cursor.execute(SQL_INSERT_FILE, args)
		self.db.commit()

	def has_file(self, hash_value):
		cursor = self.db.cursor()
		args = {
			'hash_value': hash_value
		}
		cursor.execute(SQL_HAS_FILE_BY_HASH, args)
		result = cursor.fetchone()
		if result is None:
			return False

		return True
	
	def check_file(self, hash_value, path):
		cursor = self.db.cursor()
		args = {
			'hash_value': hash_value,
			'path': path
		}
		cursor.execute(SQL_CHECK_INSERT_FILE, args)
		self.db.commit()
	
	def get_missing_files(self):
		cursor = self.db.cursor()
		missing_files = []

		for row in cursor.execute(SQL_MISSING_FILES):
			missing_files.append({
				'hash': row[0],
				'path': row[1]
			})

		return missing_files

	def get_new_files(self):
		cursor = self.db.cursor()
		missing_files = []

		for row in cursor.execute(SQL_NEW_FILES):
			missing_files.append({
				'hash': row[0],
				'path': row[1]
			})

		return missing_files
