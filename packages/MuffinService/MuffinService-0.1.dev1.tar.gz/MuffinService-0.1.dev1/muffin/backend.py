# Copyright (C) Electronic Arts Inc.  All rights reserved.

import random
from muffin.database import db
# import muffin.tables as tables


shard_id_set = set([0])  # TODO we will need one set for each project in the future
shard_map = {0: "default"}


class BackendException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def _get_cs_from_db_binding(db_binding):
    db_type = db_binding.get('type', 'sqlite')
    driver = db_binding.get('driver', None)
    user = db_binding.get('user', '')
    password = db_binding.get('password', None)
    host = db_binding.get('host', None)
    db_name = db_binding.get('db', 'muffin')

    if db_type == 'sqlite':
        db_name += '.db'
        host = None

    # dialect+driver://username:password@host:port/database
    return "{}{}://{}{}{}/{}".format(
        db_type,
        ("+" + driver) if driver is not None else "",
        user,
        (":" + password) if password is not None else "",
        ("@" + host) if host is not None else "",
        db_name)


def _init_db_bindigs(app):

    if 'SQLALCHEMY_DATABASE_URI' in app.config:
        return

    if not app.config.get('DATABASES'):
        if not app.debug:
            app.logger.warn("""No databases specified in production mode.
            Will fall back to local sqlite instance.""")

    databases = app.config.get('DATABASES', {'default': {'db': "muffin"}})
    default_db = databases.get('default')

    if default_db is None:
        raise BackendException('No default database found.')

    # setup default db binding
    app.config['SQLALCHEMY_DATABASE_URI'] = _get_cs_from_db_binding(default_db)
    del databases['default']

    # setup rest
    binds = app.config['SQLALCHEMY_BINDS'] = {}
    for k, v in databases.items():
        binds[k] = _get_cs_from_db_binding(v)

    shard_map.update(app.config.get('SHARD_MAPPINGS', shard_map))
    shard_id_set.update(set(shard_map.keys()))


def init_tables(drop_tables=False):  # pragma: no cover
    # nocover - init_tables is only used by seed and does nothing interesting
    db.reflect()

    if drop_tables:
        db.drop_all()

    db.create_all()


# def insert_projects(projects):
#     engine = _get_shard_engine(sid=None)  # get default shard
#     engine.execute(tables.projects_table.insert(), projects)


# example of how to get correct shard and id
# def get_testsuiterun(entity_id):
#     sid = get_shard_id(entity_id)
#     db_id = get_db_id(entity_id)
#     engine = _get_shard_engine(sid)
#
#      engine.execute(tables.testsuiteruns.select(), db_id)


def init_app(app):
    _init_db_bindigs(app)
    db.init_app(app)


def get_shard_id(entity_id):
    # first 32 bits are db id. 16 after is shard id. Rest is left for future.
    return (entity_id >> 32) & 0xffff


def get_db_id(entity_id):
    return entity_id & 0xffffffff


def build_entity_id(db_id, shard_id):
    return (shard_id << 32) | (db_id << 0)


# TODO Will need to pick correct shard set to randomize
def _generate_shard_id():  # pragma: no cover :
    return random.sample(shard_id_set, 1)


def _get_shard_engine(sid=None):  # pragma: no cover :
    return db.get_engine(app=None, bind=shard_map[sid] if sid is not None else None)
