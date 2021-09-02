import json
import os
import datetime
import sqlite3


# jsonファイルのディレクトリ指定
dir = os.path.dirname(__file__) + '/data/food.json'


def db_connect():
    # データベース接続
    dbname = "fooma.db"
    con = sqlite3.connect(dbname)
    # カーソルオブジェクト作成
    cur = con.cursor()
    # 接続情報の返却
    return con, cur


def db_close(con):
# 接続のコミット・クローズ
    con.commit()
    con.close()


def auth_input(name, pw):
    """
    ユーザ名が存在するか確認
    param: name: ユーザ名
    param: pw: パスワード
    """
    # データベース接続
    con, cur = db_connect()
    # userとpwが一致するデータ取得
    cur.execute("""
    SELECT * FROM `users`
        WHERE `name` = ?
        LIMIT 1
    """, (name,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # データ取得できたならユーザID，パスワード返却
    if (res==[]):
        return -1,-1
    else:
        return (res[0][0],res[0][2])


def get_user_id(name):
    """
    ユーザIDを取得
    param: name: ユーザ名
    """
    # データベース接続
    con, cur = db_connect()
    # userと一致するユーザID取得
    cur.execute("""
    SELECT `id` FROM `users`
        WHERE `name` = ?
    """, (name,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # ユーザID返却
    return res[0][0]


def get_user_name(id):
    """
    ユーザ名を取得
    param: id: ユーザID
    """
    # データベース接続
    con, cur = db_connect()
    # idと一致するユーザ名取得
    cur.execute("""
    SELECT `name` FROM `users`
        WHERE `id` = ?
    """, (id,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # ユーザ名返却
    return res[0][0]


def get_food_id(food_name):
    """
    食材IDを取得
    param: food_name: 食材の名前
    """
    # データベース接続
    con, cur = db_connect()
    # userと一致する食材ID取得
    cur.execute("""
    SELECT `id` FROM `food`
        WHERE `name` = ?
    """, (food_name,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # 食材ID返却
    return res[0][0]


def get_food_num(food_name):
    """
    食材の個数を取得
    param: food_name: 食材の名前
    """
    # データベース接続
    con, cur = db_connect()
    # foodと一致する食材の個数取得
    cur.execute("""
    SELECT `number` FROM `food`
        WHERE `name` = ?
    """, (food_name,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # 食材の個数返却
    return res[0][0]


def get_food(user_id, include_deleted = False):
    # 食材データ取得

    # データベース接続
    con, cur = db_connect()
    # 削除されていない食材データを取得
    if (include_deleted==False):
        deleted_flag = 0
    else:
        deleted_flag = 1
    cur.execute("""
    SELECT * FROM `food`
        WHERE `deleted` = ?
        and `user_id` = ?
    """, (deleted_flag, user_id,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # 食材の個数返却
    return res


def add_food(food_name, amount, user_id):
    """
    食材をデータベースに追加
    param food_name: 食材の名前
    param amount: 食材の個数
    param user_id: ユーザID
    """

    # データベースへのデータ挿入
    con, cur = db_connect()
    # 食材名がデータベースにあるか調べる
    cur.execute("""
    SELECT `name` FROM `food`
        WHERE `name` = ?
    """, (food_name,))
    _food_name = cur.fetchall()

    if (_food_name == []):
        # 食材名が重複していない場合食材を追加
        st = """
        INSERT INTO `food` (
            `name`,`number`,
            `user_id`,
            `created_at`,
            `deleted_at`,
            `deleted`) VALUES (
                ?,?,?,?,null,?)
        """
        # 食材名，個数，ユーザID，追加日時，削除日時，削除フラグ
        cur.execute(st, (food_name, amount, user_id, datetime.datetime.now(), 0,))
    else:
        # 食材名が重複していた場合は個数を加算
        # 削除済みの場合deletedを0に初期化
        food_id = get_food_id(food_name)
        food_num = get_food_num(food_name)
        st = """
        UPDATE `food`
            SET `number` = ?,
            `deleted` = 0
                WHERE `id` = ?
        """
        cur.execute(st, (food_num+int(amount), food_id,))

    # 接続クローズ
    db_close(con)


def delete(food_id):
    """
    食材購入済みによるデータ削除
    param food_name: 食材の名前
    """

    # deletedフラグの値を変更
    # 食材の数を0に初期化
    con, cur = db_connect()
    st = """
    UPDATE `food`
        SET `number` = 0,
            `deleted_at` = ?, `deleted` = ? WHERE `id` = ?
    """
    cur.execute(st, (datetime.datetime.now(), 1, food_id,))
    # 接続クローズ
    db_close(con)


def check_duplication(mail):
    """
    メールアドレスの重複確認
    param mail: メールアドレス
    """
    con, cur = db_connect()
    st = """
    SELECT * FROM `users`
        WHERE `name` = ?
    """
    cur.execute(st, (mail,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # メールアドレスが重複していたらFalseを返却
    return (res!=[])


def add_regdata(mail, enc_pw):
    """
    データベースへのユーザ情報追加
    param mail: メールアドレス
    param enc_pw: 暗号化済みパスワード
    """
    con, cur = db_connect()
    st = """
    INSERT INTO `users` (
        `name`, `pass`) values (
            ?, ?)
    """
    cur.execute(st, (mail, enc_pw,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)
