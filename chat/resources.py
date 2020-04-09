from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask import jsonify
import datetime
from flask_jwt_extended import (
    jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
from .database import db
from .models import User, UserGroup, UserChatLog, UserGroupChatLog, Friend, UserGroupMember
from .utils import datetime_format, datetime2timestamp


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
            expires = datetime.timedelta(days=30)
            access_token = create_access_token(
                identity=user.id, expires_delta=expires)
            return {'accessToken': access_token,
                    'username': user.username}, 200

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


class FriendAPI(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        friends = Friend.query.filter(
            (Friend.user == user) | (
                Friend.friend == user))
        response_data = []
        for friend in friends:
            if friend.user.id == current_user:
                data = {'fname': friend.friend.username}
            else:
                data = {'fname': friend.user.username}
            response_data.append(data)
        return {'friends': response_data}, 200

    @jwt_required
    def post(self):
        _parser = reqparse.RequestParser()
        _parser.add_argument('username',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )
        args = _parser.parse_args()
        current_user = get_jwt_identity()
        user1 = User.query.filter_by(id=current_user).first()
        user2 = User.query.filter_by(username=args['username']).first()

        friend = Friend()
        if user1.id < user2.id:
            friend.user = user1
            friend.friend = user2
        else:
            friend.user = user2
            friend.friend = user1
        db.session.add(friend)
        db.session.commit()

        return {'message': 'user %s add %s' % (
            user1.username, user2.username)}, 201


class UserGroupAPI(Resource):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        groups = UserGroup.query.filter_by(user=user)
        response_data = []
        for group in groups:
            response_data.append({
                'gname': group.gname
            })
        return {'groups': response_data}, 200

    @jwt_required
    def post(self):
        _usergroup_parser = reqparse.RequestParser()
        _usergroup_parser.add_argument('groupname',
                                       type=str,
                                       required=True,
                                       help="This field cannot be blank."
                                       )
        args = _usergroup_parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        user_group = UserGroup()
        user_group.gname = args['groupname']
        user_group.user = user
        db.session.add(user_group)
        db.session.commit()

        return {'message': 'create group %s' % user_group.gname}, 201


class UserGroupMemberAPI(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        joined_groups = UserGroupMember.query.filter_by(user=user)
        response_data = []
        for joined_group in joined_groups:
            response_data.append({
                'gname': joined_group.group.gname
            })
        return {'joined_groups': response_data}, 200

    @jwt_required
    def post(self):
        _parser = reqparse.RequestParser()
        _parser.add_argument('groupname',
                             type=str,
                             required=True,
                             help="This field cannot be blank."
                             )

        args = _parser.parse_args()
        current_user = get_jwt_identity()
        user = User.query.filter_by(id=current_user).first()
        group = UserGroup.query.filter_by(gname=args['groupname']).first()
        user_group_member = UserGroupMember()
        user_group_member.group = group
        user_group_member.user = user
        db.session.add(user_group_member)
        db.session.commit()

        return {'message': 'group %s add member %s' % (
            group.gname, user.username)}, 201


class UserChatLogAPI(Resource):
    def get(self):
        pass

    @jwt_required
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
        user_group = UserGroup()
        user_group.group_name = args['groupname']
        db.session.add(user_group)
        db.session.commit()


@socketio.on('connect')
def test_connect():
    emit('connect', {'data': 'Connected'})


@jwt_required
@socketio.on('user_chat_log')
def handle_message(username):
    user = User.query.filter_by(username=username).first()
    chatlogs = UserChatLog.query.filter_by(
        to_user=user).group_by(UserChatLog.from_user_id)
    response_data = []
    if chatlogs:
        for chatlog in chatlogs:
            data = {
                'from_user': chatlog.from_user.username,
                'message': chatlog.message,
                'create_time': datetime2timestamp(chatlog.create_time),
                'display_time': datetime_format(chatlog.create_time)
            }
            response_data.append(data)
    emit("on_response", response_data)


@jwt_required
@socketio.on('group_chat_log')
def group_chat_log(gname):
    group = Group.query.ilter_by(gname=gname).first()
    chatlogs = GroupChatLog.query.filter_by(group=group)
    response_data = []
    if chatlogs:
        for chatlog in chatlogs:
            data = {
                'from_user': chatlog.from_user.username,
                'message': chatlog.message,
                'create_time': datetime2timestamp(chatlog.create_time),
                'display_time': datetime_format(chatlog.create_time)
            }
            response_data.append(data)
    emit("on_response", response_data, broadcast=True)


@socketio.on('user_chat_dialog')
def user_chat_dialog(contact, current_user):
    contact = User.query.filter_by(username=contact).first()
    current_user = User.query.filter_by(username=current_user).first()
    dialogs = UserChatLog.query.filter(
        ((UserChatLog.to_user == contact) & (
            UserChatLog.from_user == current_user)) | (
            (UserChatLog.from_user == contact) & (
                UserChatLog.to_user == current_user))).order_by(
                    UserChatLog.create_time)
    response_data = []
    if dialogs:
        for dialog in dialogs:
            data = {
                'from_user': dialog.from_user.username,
                'to_user': dialog.to_user.username,
                'message': dialog.message,
                'create_time': datetime2timestamp(dialog.create_time),
                'display_time': datetime_format(dialog.create_time)
            }
            response_data.append(data)
    room = current_user.id
    join_room(room)
    emit("on_response", response_data, room=room)


@socketio.on('group_chat_dialog')
def group_chat_dialog(gname):
    group = UserGroup.query.filter_by(gname=gname).first()
    dialogs = UserGroupChatLog.query.filter_by(
        group=group).order_by(
        UserGroupChatLog.create_time)
    response_data = []
    if dialogs:
        for dialog in dialogs:
            data = {
                'user': dialog.user.username,
                'message': dialog.message,
                'create_time': datetime2timestamp(dialog.create_time),
                'display_time': datetime_format(dialog.create_time)
            }
            response_data.append(data)
    room = group.id
    join_room(room)
    emit("on_response", response_data, room=room)


@socketio.on('send_user_message')
def handle_user_message(from_username, to_username, message):
    from_user = User.query.filter_by(username=from_username).first()
    to_user = User.query.filter_by(username=to_username).first()
    chatlog = UserChatLog(
        to_user=to_user,
        from_user=from_user,
        message=message)
    db.session.add(chatlog)
    db.session.commit()
    room = from_user.id
    data = {
        'from_user': chatlog.from_user.username,
        'to_user': chatlog.to_user.username,
        'message': chatlog.message,
        'create_time': datetime2timestamp(chatlog.create_time),
        'display_time': datetime_format(chatlog.create_time)
    }
    emit("user_message", data, room=room)


@socketio.on('send_group_message')
def handle_group_message(username, gname, message=None):
    user = User.query.filter_by(username=username).first()
    group = UserGroup.query.filter_by(gname=gname).first()
    chatlog = UserGroupChatLog(
        user=user,
        group=group,
        message=message)
    db.session.add(chatlog)
    db.session.commit()
    data = {
        'user': chatlog.user.username,
        'group': chatlog.group.gname,
        'message': chatlog.message,
        'create_time': datetime2timestamp(chatlog.create_time),
        'display_time': datetime_format(chatlog.create_time)
    }
    room = group.id
    emit("group_message", data, room=room)


@socketio.on('search')
def handle_search(username, search_value, search_type):
    print(username)
    current_user = User.query.filter_by(username=username).first()
    response_data = []
    if search_type == 'friend':
        users = User.query.filter(User.username.contains(search_value))
        if users:
            for user in users:
                if current_user.id < user.id:
                    friend = Friend.query.filter_by(
                        user=current_user, friend=user).first()
                else:
                    friend = Friend.query.filter_by(
                        user=user, friend=current_user).first()
                if not friend:
                    response_data.append({
                        'username': user.username
                    })

    elif search_type == 'group':
        groups = UserGroup.query.filter(UserGroup.gname.contains(search_value))
        if groups:
            for group in groups:
                response_data.append({
                    'gname': group.gname
                })

    emit('search_result', response_data)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('error')
def test_disconnect():
    print('socket.io error')


api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(UserGroupAPI, '/group', endpoint='group')
api.add_resource(FriendAPI, '/friend', endpoint='friend')
api.add_resource(UserGroupMemberAPI, '/groupmember', endpoint='groupmemeber')
api.add_resource(UserGroupMemberAPI, '/joinedgroup', endpoint='groupjoined')
