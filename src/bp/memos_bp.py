from flask import Blueprint, request
from .home_bp import Memos, db
from .err_bp import handle_bad_input_501, handle_server_500
from sqlalchemy.orm import sessionmaker, scoped_session

# validates that curr_memo_id in db:
def memo_id_validation(curr_memo_id):
    return db.session.query(db.exists().where(Memos.id == curr_memo_id)).scalar()


def get_new_memo_id():
    
    # generate memo id using gen_memo_id (according gen_memo_id defenitions):
    gen_rand_memo = Memos.gen_memo_id()

    # validate that gen_rand_memo not exists in the db:
    while db.session.query(db.exists().where(Memos.id == gen_rand_memo)).scalar():
         gen_rand_memo = Memos.gen_memo_id()

    return gen_rand_memo

    
def get_msg(memo_id):
    
    try:
        ret_msg = db.session.query(Memos).get(memo_id).msg
        if not ret_msg:
            return "There is no message for memo id " + memo_id
        else:
            return "The message for memo id " + str(memo_id) + " is: " + ret_msg
    
    except:
         return handle_server_500(f"There was an issue retriving the message for memo id: {memo_id}")


memos_blueprint = Blueprint('memos', __name__)

# handles invalid requests:
@memos_blueprint.route("/memo_id", methods=["POST", "PUT", "DELETE"])
def handle_memo_id_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for memo_id url!")


@memos_blueprint.route("/memo_id", methods=["GET"])
def memo_id_generator():
    
    # configure db and get a memo id:
    new_memo_id = get_new_memo_id()

    # create new memo with the generated memo id:
    new_memo = Memos(new_memo_id)
    
    # save the memo in the db:
    try:
        
        # creating an infra route to the db engine: 
        sm = sessionmaker(bind=db.engine)

        # creating thread-specific memo of sm - handles multiple access to the same sm, using sm to create a memo:
        session = scoped_session(sm)

        # adding and commiting new_memo to db using the local scoped_session:
        session.add(new_memo)
        session.commit()
        return repr(new_memo), 201

    except:
            return handle_server_500("There was an issue adding new memo id to the db!")

    finally:
        session.close()


# handles invalid requests:
@memos_blueprint.route("/memo_msg", methods=["POST", "PUT", "DELETE"])
def handle_memo_msg_forbidden_requests():
    return handle_bad_input_501("This method is forbidden for memo msg url!")


# retriving the message of a provided memo_id:
@memos_blueprint.route("/memo_msg", methods=["GET"])
def get_memo_msg():
    
    # retriving the memo_id from the request:
    curr_memo_id = request.args.get("memo_id")

    if memo_id_validation(curr_memo_id) is False:
        return handle_bad_input_501(f"The provided memo id {curr_memo_id} isn't valid!")
    return get_msg(curr_memo_id)

    