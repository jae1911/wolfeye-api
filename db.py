from peewee import *

from playhouse.migrate import *

database = SqliteDatabase('db/search.db')

def migrate_db():
	migrator = SqliteMigrator(database)
	try:
		description = TextField(default='')
		migrate(
			migrator.add_column('search', 'description', description)
		)
	except:
		pass


class BaseModel(Model):
	""" Base to be used by other tables
	"""

	class Meta:
		database = database

class Search(BaseModel):
	title = CharField()
	url = CharField()
	last_fetched = DateTimeField()
	description = TextField()

class Token(BaseModel):
	token = CharField()
	expiry_date = DateTimeField()
