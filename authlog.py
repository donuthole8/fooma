from flask import session
import data


def is_login():
    # ログインしているか確認
    return 'user' in session


def auth_param(user, pw):
    # ユーザとパスワードが合っているか認証する
    print('auth_param')

    # ユーザ名とパスワードが合っているか確認する
    user_id = data.auth_input(user,pw)
    if (user_id==-1):
        return False

    # セッションに値を保存
    session['user'] = user_id
    # 認証成功
    return True


def logout():
    # ログアウト
    session.pop('user', None)
