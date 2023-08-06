# Copyright (C) Electronic Arts Inc.  All rights reserved.

import pytest
from muffin.factories import create_app

import muffin.backend as be


@pytest.fixture()
def app(request):
    application = create_app('muffin.testing.cfg')
    application.config['TESTING'] = True

    ctx = application.app_context()
    ctx.push()

    def finalize():
        ctx.pop()

    request.addfinalizer(finalize)
    application.logger.disabled = True

    return application


@pytest.fixture()
def test_backend(app):  # pylint:disable=W0621
    be.init_app(app)
    be.init_tables(drop_tables=True)
    return be
