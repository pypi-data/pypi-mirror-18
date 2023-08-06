# Copyright (C) Electronic Arts Inc.  All rights reserved.

import time
import random
from flask_script import Command
import flask
import muffin.backend as backend


class SeedDatabase(Command):
    # command method
    def run(self):  # pylint: disable=E0202
        app = flask.current_app
        random.seed(123)

        print("seeding database...")
        start = time.clock()
        backend.init_app(app)
        backend.init_tables(drop_tables=True)

        # backend.insert_projects()

        print("done, elapsed time: {}s".format((time.clock() - start)))
