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
    ユーザ名とパスワードが合っているか確認
    param: name: ユーザ名
    param: pw: パスワード
    """
    # データベース接続
    con, cur = db_connect()
    # userとpwが一致するデータ取得
    cur.execute("""
    SELECT * FROM `users`
        WHERE `name` = ?
        AND `pass` = ?
        LIMIT 1
    """, (name, pw,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # データ取得できたならユーザID返却
    if (res==[]):
        return -1
    else:
        return (res[0][0])


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


def get_food(include_deleted = False):
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
    """, (deleted_flag,))
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    # 食材のデータ返却
    return res


def get_food_price():
    # 食材データと金額データ取得

    # データベース接続
    con, cur = db_connect()
    cur.execute("""
    SELECT * FROM `food`
        LEFT JOIN `purchases`
            ON food.id = purchases.food_id
                LEFT JOIN `users`
                    ON purchases.user_id = users.id
    """)
    res = cur.fetchall()
    # 接続クローズ
    db_close(con)

    print("res")
    print(res)
    print("end")

    # 食材のデータと金額返却
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

    db_close(con)
    con, cur = db_connect()

    if (_food_name == []):
        # 食材名が重複していない場合食材を追加
        st = """
        INSERT INTO `food` (
            `name`,
            `number`,
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


def price_validation(price):
    """
    入力金額のバリデーション
    param price: 金額
    """

    # 入力されていない場合0円とする
    if (price==""):
        price = 0

    # 有効な値であるかチェック
    if not (str(price).isnumeric()):
        return -1,False

    # 有効であれば金額を返却
    return int(price), True


def add_price(price, food_name, food_num, user_id):
    """
    入力金額をデータベースへ追加
    param price: 金額
    param food_name: 食材名
    param food_num: 食材個数
    param user_id: ユーザID
    """

    # ユーザIDと食材の組み合わせが既存であるか調べる
    con, cur = db_connect()
    st = """
    SELECT * FROM `purchases`
        WHERE `user_id` = ?
            AND `food_id` = ?
    """
    cur.execute(st, (user_id, get_food_id(food_name),))
    res = cur.fetchall()

    db_close(con)
    con, cur = db_connect()

    if (res==[]):
        # 入力金額×個数をデータベースへ追加
        st = """
        INSERT INTO `purchases` (
            `user_id`,
            `food_id`,
            `price`) VALUES (
                ?,?,?)
        """
        cur.execute(st, (user_id,get_food_id(food_name),int(price)*int(food_num),))
    else:
        # 入力金額×個数をデータベースに加算
        st = """
            UPDATE `purchases`
                SET `price` = `price` + ?
                    WHERE `user_id` = ?
                        AND `food_id` = ?
        """
        cur.execute(st, (int(price)*int(food_num),user_id,get_food_id(food_name),))

    # 接続クローズ
    db_close(con)


def reset_price(user_id,food_id):
    """
    金額を0円にリセットする
    param user_id: ユーザID
    param food_id: 食材ID
    """

    # 金額を0円に更新する
    con, cur = db_connect()
    st = """
        UPDATE `purchases`
            SET `price` = 0
                WHERE `user_id` = ?
                    AND `food_id` = ?
    """
    cur.execute(st, (user_id,food_id,))
    db_close(con)
