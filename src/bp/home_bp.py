from flask import Blueprint
from .err_bp import handle_server_500
from project.memos import db, Memos

# validates that the provided json file includes mandatory fields: 
def validate_json_keys(json_data):
    keys_dict = json_data.keys()
    must_have_keys = ["message", "additional", "level", "timestamp", "fileName", "lineNumber"]

    if (all(map(lambda provided_json_keys: True if provided_json_keys in keys_dict else False, must_have_keys))):
        return True

    ret_str = "The following key/s are missing:\n"
    for key in keys_dict:
        if key in must_have_keys:
            must_have_keys.remove(key)

    ret_str += str(must_have_keys).strip('[]')
    return ret_str
        

# sets the provided msg in the db, handles overriding data:
def set_msg(memo_id, msg):
    
    try:
        ret_val = ""
        memo_update = db.memo.query(Memos).get(memo_id)
        if memo_update.msg :
            ret_val = "Overriding message for memo id: " + memo_id + ", previous message was: " + memo_update.msg + "\n"
        memo_update.msg = msg
        db.memo.commit()
        return ret_val

    except:
        return handle_server_500(f"There was an issue adding message to a memo id: {memo_id}")


# blueprint for home page of demystify project:
home_blueprint = Blueprint('home', __name__)


@home_blueprint.route("/")
def home():
    return "Main memos project page!!! NEW YEAR 2024!"

    
