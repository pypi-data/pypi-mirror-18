# Copyright (C) Electronic Arts Inc.  All rights reserved.

import logging
from flask import Flask
from werkzeug.contrib.profiler import ProfilerMiddleware

import muffin.backend as backend
import muffin.muffin_error as muffin_error
from muffin.v2 import register_api as register_api


def create_app(config_file):
    app = Flask("muffin")
    app.config.from_pyfile(config_file)

    if app.debug:
        app.logger.setLevel(logging.DEBUG)

    # set up wanted middleware
    if app.config.get('PROFILE', False):  # pragma: no cover
        # no-cover we don't want to verify profile configs
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[10])

    # init backend
    backend.init_app(app)

    # install error handlers
    app.register_blueprint(muffin_error.muffin_error)

    # register api blueprints
    register_api(app, url_prefix="/api/v2")

    return app
