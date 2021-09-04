from flask import Flask, request, redirect, render_template, session
import data
import authlog
import reguser
import os


# Flaskインスタンスの作成
app = Flask(__name__)
# セッションキーの設定
app.secret_key = 'Lomd0nUthOlE'


@app.context_processor
# CSSがキャッシュにより反映されない問題を解消
def add_staticfile():
    def staticfile_cp(fname):
        path = os.path.join(app.root_path, 'static', fname)
        mtime =  str(int(os.stat(path).st_mtime))
        return '/static/' + fname + '?v=' + str(mtime)
    return dict(staticfile=staticfile_cp)


def ret_fooma():
    # fooma.htmlのテンプレートを返却
    # food_data = data.get_food(session['user'])
    food_data = data.get_food_price()
    leng = len(food_data)
    bought_user = []
    for i in food_data:
        bought_user.append(i[11])
    print('bought_user',bought_user)

    return render_template('fooma.html',
        user = data.get_user_name(session['user']),
        leng = leng,
        data = food_data,
        bought_user = bought_user
    )


@app.route('/')
def login():
    # ログイン画面
    print('start /')
    return render_template('login.html')


@app.route('/auth', methods=['POST'])
def auth():
    # ログイン認証
    print('start auth')

    # フォームの値を習得
    user, pw = None, None
    if 'user' in request.form:
        user = request.form['user']
    if 'pw' in request.form:
        pw = request.form['pw']
    if (user is None) or (pw is None):
        return redirect('/')
    print('user,pw inputed')
    print(user,pw)

    # ユーザ情報が認証されたときfooma.html（メイン画面）を返す
    if authlog.auth_param(user, pw) == True:
        print('user,pw authed')
        return ret_fooma()
    # ユーザ情報が誤っていたときerror.html（認証エラー画面）を返す
    else:
        print('auth failed')
        return render_template('error.html')


@app.route('/add', methods=['POST'])
def add():
    # 食材追加処理
    print('start add')

    # セッションからユーザID取得
    user = session['user']

    # フォームの値を習得
    if not request.form['food']:
        # エラーメッセージを返却しても良い
        return ret_fooma()
    else:
        food = request.form['food']
    num = request.form['num']
    price = 0
    if request.form['price']:
        price = request.form['price']

    # 食材をデータベースに追加
    data.add_food(food, num, user)
    data.add_price(price, food, num, user)
    print('food added')

    return ret_fooma()


@app.route('/bought', methods=['POST'])
def bought():
    # 食材購入済み処理
    print('start bought')

    # フォームの値を習得
    if not request.form['bought_food']:
        return ret_fooma()
    else:
        food_id = request.form['bought_food']

    # 購入済み食材をdeletedフラグ立てる
    data.delete(food_id)

    return ret_fooma()


@app.route('/logout')
def logout():
    # ログアウト
    print('logout')
    authlog.logout()

    return redirect('/')


@app.route('/register')
def register():
    # 新規ユーザ登録
    print('register')

    return render_template('register.html')


@app.route('/user/store', methods=['POST'])
def check_register():
    # ユーザ登録情報確認
    print('check_register')

    # フォームの値を習得
    mail,pw,pw_check = None,None,None
    if 'mail' in request.form:
        mail = request.form['mail']
    if 'pw' in request.form:
        pw = request.form['pw']
    if 'pw-check' in request.form:
        pw_check = request.form['pw-check']
    print('mail,pw,pw-check inputed')

    # バリデーション
    msg,isCorrect = reguser.validation(mail, pw, pw_check)

    print(msg,isCorrect)

    if not isCorrect:
        return render_template('register.html', msg=msg)

    # セッションに新規ユーザID保存
    authlog.save_session(data.get_user_id(mail))

    # ユーザ登録の認証機能が完成したらメイン画面へ移行
    return ret_fooma()


if __name__ == '__main__':
    # アプリ起動
    app.run(host="0.0.0.0")
