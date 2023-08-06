# Copyright (C) Electronic Arts Inc.  All rights reserved.

from muffin.database import db

projects_table = db.Table('projects',
                          db.Column('project_id', db.Integer, primary_key=True),
                          db.Column('name', db.String(150)),
                          info={'bind_key': None})

# shard_set contains information such as name, and other misc stuff.
# A shard_set points to another table with a list of all the shards it contains.
# A project points to one write shard_set and another read shard_set.
# Both read and write can point to the same shard_set.
