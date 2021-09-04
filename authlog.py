from flask import session
from flask_bcrypt import Bcrypt
import data


def is_login():
    # ログインしているか確認
    return 'user' in session


def save_session(user_id):
    # セッションに値を保存
    session['user'] = user_id


def auth_param(user, pw):
    # ユーザとパスワードが合っているか認証する
    print('auth_param')

    # ユーザ名が存在するか確認する
    user_id,enc_pw = data.auth_input(user)
    if (user_id==-1):
        return False

    # パスワードが合っているか確認する
    bcrypt = Bcrypt()
    if not (bcrypt.check_password_hash(enc_pw, pw)):
        return False

    # セッションに値を保存
    save_session(user_id)
    # 認証成功
    return True


def logout():
    # ログアウト
    session.pop('user', None)
