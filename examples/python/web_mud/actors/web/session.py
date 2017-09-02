from flask import session as flask_session


def set_avatar_to_session(avatar_id: int):
    flask_session['avatar'] = avatar_id


def get_avatar_id_from_session():
    return flask_session.get('avatar', None)


def set_state(state: str, value: str):
    flask_session[state] = value


def get_state(state: str, default: str = ''):
    return flask_session.get(state, default)
