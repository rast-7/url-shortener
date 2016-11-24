from peewee import *

db = SqliteDatabase('urls.db')

class weburls(Model):
	id = PrimaryKeyField()
	url = TextField()
	
	class Meta:
		database = db
		
def initialize_db():
	db.connect()
	db.create_tables([weburls],safe=True)

