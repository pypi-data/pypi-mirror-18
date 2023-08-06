# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask_script

import muffin.factories
import muffin.manage.seed as mg

application = muffin.factories.create_app('muffin.cfg')

manager = flask_script.Manager(application)
manager.add_command('seed', mg.SeedDatabase)

if __name__ == "__main__":
    manager.run()
