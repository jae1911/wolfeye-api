""" This is the module that manages the database operations.
    Current ORM is called Peewee.
"""

import logging
import peewee

from playhouse import migrate

db_logger = logging.getLogger('database')

database = peewee.SqliteDatabase('db/search.db')

def migrate_db():
    """ Migrate the database to get new tables
    """
    migrator = migrate.SqliteMigrator(database)
    try:
        description = peewee.TextField(default='')
        migrate.migrate(
            migrator.add_column('search', 'description', description)
        )
    except peewee.OperationalError:
        db_logger.warning("Could not migrate database, maybe already migrated?")


class BaseModel(peewee.Model): # pylint: disable=too-few-public-methods
    """ Base to be used by other tables
    """

    class Meta: # pylint: disable=too-few-public-methods
        """ Default peewee metal class to set the database used
        """
        database = database

class Search(BaseModel): # pylint: disable=too-few-public-methods
    """ Default table that stores the search results
    """
    title = peewee.CharField()
    url = peewee.CharField()
    last_fetched = peewee.DateTimeField()
    description = peewee.TextField()

class Token(BaseModel): # pylint: disable=too-few-public-methods
    """ Table that stores the admin tokens
    """
    token = peewee.CharField()
    expiry_date = peewee.DateTimeField()
