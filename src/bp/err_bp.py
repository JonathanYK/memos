from flask import Blueprint

# blueprint that represent handling errors: 
err_blueprint = Blueprint('err', __name__)

@err_blueprint.errorhandler(404)
def handle_bad_request_404(_):
    return "Bad request! Resource not found.", 404

@err_blueprint.errorhandler(500)
def handle_server_500(err_msg):
    return err_msg, 500

@err_blueprint.errorhandler(501)
def handle_bad_input_501(err_msg):
    return err_msg, 501

    