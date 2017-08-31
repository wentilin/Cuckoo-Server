from functools import wraps
from flask import request
from services.account_service import AccountService
from api.errors import APIError
from flask import jsonify
from functools import wraps
from flask import Blueprint

api = Blueprint('api', __name__, url_prefix='/api/v1')
img_api = Blueprint('img_api', __name__)


@api.app_errorhandler(500)
def internal_server_error(e):
    if isinstance(e, APIError):
        return jsonify(code=e.code, data=e.data, msg=e.msg)

    return jsonify(code=500, data=e.__cause__, msg='服务器内部发生错误')


def auth_required(func):
    @wraps(func)
    def decorator(*args, **kw):
        auth(request)
        return func(*args, **kw)

    return decorator


def auth(request):
    '''
    验证请求
    '''
    auth_code = request.headers.get('Authorization')
    date = request.headers.get('Date')
    if auth_code is None:
        raise APIError(code=500001, msg='missing headers!')

    if not do_auth(request, auth_code, date):
        raise APIError(code=406, msg='auth failed!')


def do_auth(request, auth_code, date):
    '''
    处理验证
    '''
    tokens = auth_code.split(':')
    if len(tokens) < 3:
        return False

    device = int(tokens[0])
    uid = int(tokens[1])
    code = tokens[2]

    user = AccountService().auth(uid, device, code, date)
    if user is None:
        return False

    user.device = device
    request.__user__ = user

    return True

from api import account, comment, feed, friend, image, user
