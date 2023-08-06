# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask

muffin_error = flask.Blueprint('muffin_error', __name__)


class MuffinError(Exception):

    def __init__(self, message, payload=None, status_code=None):
        super().__init__(self)
        self.message = message
        self.payload = payload
        self.status_code = status_code or 400
        import traceback
        self.stack_trace = traceback.format_exc()

    def to_dict(self):
        d = dict(self.payload or ())
        d['message'] = self.message
        d['statusCode'] = self.status_code
        d['stackTrace'] = self.stack_trace
        return d


@muffin_error.app_errorhandler(MuffinError)
def handle_muffin_error(error):
    print("Error handler invoked")
    response = flask.jsonify(error.to_dict())
    response.status_code = error.status_code

    print(response)
    return response


@muffin_error.app_errorhandler(404)
def handle_404(error):
    del error
    response = flask.jsonify(
        {"message": "the requested resource could not be found.", "statusCode": 404}
    )
    response.status_code = 404

    return response


@muffin_error.app_errorhandler(400)
def handle_400(error):
    response = flask.jsonify(
        {"message": "bad request: {}".format(error), "statusCode": 400},
    )
    response.status_code = 400

    return response


# log all 500 errors
@muffin_error.app_errorhandler(500)
def handle_500(error):
    import traceback
    stack_trace = traceback.format_exc()

    response = flask.jsonify(
        {"message": "an internal server error occurred.",
         "statusCode": 500,
         "stackTrace": stack_trace}
    )
    response.status_code = 500

    flask.current_app.logger.exception(error)

    return response
