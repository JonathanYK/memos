import logging
import os
from flask import Blueprint, request
from .err_bp import handle_bad_input_501
from .home_bp import set_msg, validate_json_keys
from .memos_bp import memo_id_validation

def log_level_validation(cur_log_level):
    return cur_log_level in {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG", "NOTSET"}


# dynamic methods, each for the appropriate level:
def print_CRITICAL(logger, logging_data):
    for data in logging_data: logger.critical(data)


def print_ERROR(logger, logging_data):
    for data in logging_data: logger.error(data)


def print_WARNING(logger, logging_data):
    for data in logging_data: logger.warning(data)


def print_INFO(logger, logging_data):
    for data in logging_data: logger.info(data)


def print_DEBUG(logger, logging_data):
    for data in logging_data: logger.debug(data)


def print_NOTSET(logger, logging_data):
    for data in logging_data: logger.notset(data)


# logging the data to a .log file:
def log_data(logger, memo_id, json_data):

    # list for relevant logging params:
    logging_data = []

    # parsering the json params:
    str_log_level = json_data["level"]
    
    # validate str_log_level:
    if log_level_validation(str_log_level) is False:
        return handle_bad_input_501("The provided log level isn't valid!")

    logging_data.append(str_log_level)
    logging_data.append(json_data["timestamp"])
    logging_data.append(json_data["fileName"])
    logging_data.append(json_data["lineNumber"])

    # create log level printings according to provided log level, then set the same log level:
    dynamic_log_printer = globals()["print_%s" % str_log_level]
    logger.setLevel(logging.getLevelName(str_log_level))

    # config memo formatter both for file_handler and stream_handler:
    memo_formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(name)s::%(message)s")
    
    # file_handler configurations:
    log_filename = f'logging/{memo_id}.log'
    os.makedirs(os.path.dirname(log_filename), exist_ok=True)

    file_handler = logging.FileHandler(filename=log_filename, mode="a")
    file_handler.set_name(memo_id)
    file_handler.setFormatter(memo_formatter)

    # stream_handler configurations:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(memo_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # dynamic printing to the relevant log:
    dynamic_log_printer(logger, logging_data)

    # removing both file and stream handlers, in order to avoid duplications:
    logger.removeHandler(file_handler)
    logger.removeHandler(stream_handler)

log_blueprint = Blueprint('log', __name__)


# handles invalid requests:
@log_blueprint.route("/log", methods=["GET", "PUT", "DELETE"])
def handle_memo_log_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for log url!")

# handles posting log to db:
@log_blueprint.route("/log", methods=["POST"])
def log():

    ret_val = ""

    # retriving the memo id from the url:
    curr_memo_id = request.args.get("memo_id")

    # validate the memo id:
    if memo_id_validation(curr_memo_id) is False:
        return handle_bad_input_501("The provided memo id isn't valid!")

    # validate there arn't missing required keys in json file:
    json_valid = validate_json_keys(request.json)
    if json_valid is not True:
        return handle_bad_input_501(json_valid)

    logger = logging.getLogger("__name__")

    curr_msg = request.json["message"]
    ret_val+=set_msg(curr_memo_id, curr_msg)

    # log the data to a dedicated file (memo_id.log):
    log_data(logger, curr_memo_id, request.json)

    ret_val+=f"logging memo id: {str(curr_memo_id)} done!"
    return ret_val

