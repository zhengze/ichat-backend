from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO, emit
from flask import jsonify
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import json
from .database import db
from .models import User, UserGroup, UserChatLog, UserGroupChatLog


chat_bp = Blueprint('chat', __name__)
api = Api(chat_bp)
socketio = SocketIO(cors_allowed_origins="*")


class Login(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('username',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        args = _user_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.check_password(args['password']):
            access_token = create_access_token(identity=user.id)
            return {'accessToken': access_token}, 200

        return {'message': 'invalid'}, 401


class Register(Resource):
    def post(self):
        _user_parser = reqparse.RequestParser()
        _user_parser.add_argument('username',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        _user_parser.add_argument('password',
                                  type=str,
                                  required=True,
                                  help="This field cannot be blank."
                                  )
        args = _user_parser.parse_args()
        user = User(args['username'], args['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'create user %s' % user.username}, 201


class Logout(Resource):
    def post(self):
        pass


class UserGroupAPI(Resource):
    def get(self):
        pass

    def post(self):
        _usergroup_parser = reqparse.RequestParser()
        _usergroup_parser.add_argument('groupname',
                                       type=str,
                                       required=True,
                                       help="This field cannot be blank."
                                       )
        args = _usergroup_parser.parse_args()
        user_group = UserGroup()
        user_group.group_name = args['groupname']
        db.session.add(user_group)
        db.session.commit()

        return {'message': 'create group %s' % user_group.group_name}, 201

# chat_bp.route("/chat")
# def chat():
#    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
#    user_socket_list.append(user_socket)
#    print(len(user_socket_list), user_socket_list)
#    try:
#        while True:
#            msg = user_socket.receive()
#            for socket in user_socket_list:
#                if socket != user_socket_list:
#                    socket.send(json.dumps({"msg": msg})) # " 服务器信息: " +
#    except WebSocketError as e:
#        print(e)
#        user_socket_list.remove(user_socket)
#        return ''


class UserChatLogAPI(Resource):
    def get(self):
        pass

    def post(self):
        _parser = reqparse.RequestParser()
        _parser.add_argument('from_user',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )
        _parser.add_argument('to_user',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )
        args = _parser.parse_args()
        args = _usergroup_parser.parse_args()
        user_group = UserGroup()
        user_group.group_name = args['groupname']
        db.session.add(user_group)
        db.session.commit()


user_socket_list = []


class UserChatAPI(Resource):
    def get(self):
        pass

    def post(self):
        user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
        user_socket_list.append(user_socket)
        print(len(user_socket_list), user_socket_list)
        try:
            while True:
                msg = user_socket.receive()
                for socket in user_socket_list:
                    if socket != user_socket_list:
                        socket.send(json.dumps({"msg": msg}))  # " 服务器信息: " +
        except WebSocketError as e:
            print(e)
            user_socket_list.remove(user_socket)
            return ''


class GroupChatLogAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass


class GroupChatAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass


class ContactAPI(Resource):
    def get(self):
        pass

    def post(self):
        pass


@socketio.on('connect')
def test_connect():
    emit('connect', {'data': 'Connected'})


@socketio.on('user_chat_log')
def handle_message(username):
    user = User.query.filter_by(username=username).first()
    chatlog = UserChatLog.query.filter_by(to_user=user).first()
    data = {
        'from_user': chatlog.from_user.username,
        'message': chatlog.message,
        'create_time': '18:30'
    }
    emit("on_response", data)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(UserGroupAPI, '/group', endpoint='group')
api.add_resource(UserChatAPI, '/userchat', endpoint='user_chat')
api.add_resource(UserChatLogAPI, '/userchatlog', endpoint='user_chat_log')
api.add_resource(GroupChatAPI, '/groupchat', endpoint='group_chat')
api.add_resource(GroupChatAPI, '/groupchatlog', endpoint='group_chat_log')
