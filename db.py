from peewee import *

database = SqliteDatabase('search.db')

class BaseModel(Model):
	""" Base to be used by other tables
	"""

	class Meta:
		database = database

class Search(BaseModel):
	title = CharField()
	url = CharField()
	last_fetched = DateTimeField()
