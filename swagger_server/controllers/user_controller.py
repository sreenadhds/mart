import connexion
import six

from swagger_server.models.user import User  # noqa: E501
from swagger_server import util
from swagger_server.models import orm
from connexion import NoContent
from swagger_server import globals
from functools import wraps
from swagger_server.util import verify_password,parse_cookie,generate_cookie,encode_password_token,decode_password_token

import jwt
import logging
logger = logging.getLogger('connexion.apis.flask_api')


def login_needed(f):
    """
    validate login
    :param f:
    :return:
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        authenticated_token=[]
        logging.info(args)
        if 'Cookie' in connexion.request.headers:
            logging.info(type(connexion.request.headers['Cookie']))
            authenticated_token=parse_cookie(connexion.request.headers['Cookie'],'Autorization')
        if authenticated_token:
            try:
                decode_val=decode_password_token(authenticated_token[0])
                logging.info("Authentication successful for user %s",decode_val['username'])
                return f(*args, **kwargs)
            except Exception as e:
                logging.error(e)
        return "login required /login",302


    return wrap

# @login_needed
def create_user(body):  # noqa: E501
    """Create user

    This can only be done by the logged in user. # noqa: E501

    :param body: Created user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        user = {"id": body.id, "dao_username": body.username, "dao_firstname": body.first_name,
                "dao_lastname": body.last_name, "dao_email": body.email,
                "dao_password": util.generate_hash(body.password)}
        if user is not None:
            logging.info("Adding user %s", user)
            globals.db_session.add(orm.Userinfo(**user))
            globals.db_session.commit()
            logging.info("user commit %s successful", user)
            return "User added", 200

    except Exception as e:
        logging.error(e)

    return NoContent, 404

@login_needed
def delete_user(username):  # noqa: E501
    """Delete user

    This can only be done by the logged in user. # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: None
    """
    try:
        logging.info("Getting username for delete %s", username)
        user = globals.db_session.query(orm.Userinfo).filter(orm.Userinfo.dao_username == username).first()
        if user is not None:
            globals.db_session.delete(user)
            globals.db_session.commit()
            return NoContent, 200
        else:
            return "User not found", 404
    except Exception as e:
        logging.error(e)

    return "Invalid username supplied", 400

def get_user_by_name(username):  # noqa: E501
    """Get user by user name

     # noqa: E501

    :param username: The name that needs to be fetched. Use user1 for testing. 
    :type username: str

    :rtype: User
    """
    try:
        logging.info("Getting username %s", username)
        user = globals.db_session.query(orm.Userinfo).filter(orm.Userinfo.dao_username == username).first()
        logging.debug("Got username %s response %s", username, user.__dict__)
        if user is not None:
            return User.from_dict(
                dict(id=user.id, username=user.dao_username, firstname=user.dao_firstname, email=user.dao_email,
                     lastName=user.dao_lastname)), 200
        else:
            return "User not found", 404
    except Exception as e:
        logging.error(e)

    return "Invalid username supplied", 400

@login_needed
def update_user(username, body):  # noqa: E501
    """Updated user

    This can only be done by the logged in user. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Updated user object
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        logging.info("Getting username for update %s", username)
        user = globals.db_session.query(orm.Userinfo).filter(orm.Userinfo.dao_username == username).first()
        logging.debug("Got username for update %s response %s", username, user.__dict__)
        if user is not None:
            user = {"id": body.id, "dao_username": body.username, "dao_firstname": body.first_name,
                    "dao_lastname": body.last_name, "dao_email": body.email,
                    "dao_password": util.generate_hash(body.password)}
            globals.db_session.query(orm.Userinfo).filter(orm.Userinfo.dao_username == username).update(user)
            globals.db_session.commit()

            return NoContent, 200
        else:
            return "User not found", 404
    except Exception as e:
        logging.error(e)

    return "Invalid username supplied", 400

def authenticate_login(body):
    if connexion.request.is_json:
        body = User.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        user = globals.db_session.query(orm.Userinfo).filter(orm.Userinfo.dao_username == body.username).first()
        if user is None:
            logging.info("Invalid user provided for authentication %s",body)
            return 'Unauthorized',403
        #check password matches
        if verify_password(user.dao_password,body.password):
            logging.info("User %s verification done",user.__dict__)
            logging.info("setting auth cookies for user %s",user.__dict__)
        #do Jwt implementation
            hashed_token = encode_password_token(connexion.request.get_json())
            return 'success', 200, generate_cookie("Autorization",hashed_token)

    except Exception as e:
        logging.error(e)

    return 'Unauthorized', 403