# データベースのテーブル作成用プログラム

import sqlite3

# データベース接続
dbname = "fooma.db"
con = sqlite3.connect(dbname)

# カーソルオブジェクト作成
cur = con.cursor()
# ユーザテーブル作成
# st = """
#     CREATE TABLE `users` (
#         `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#         `name` VARCHAR(128) NOT NULL,
#         `pass` VARCHAR(128) NOT NULL)
#     """
# cur.execute(st)
# # 食材テーブル作成
# st = """
#     CREATE TABLE `food` (
#         `id` iNTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#         `name` VARCHAR(128) NOT NULL,
#         `number` INT NOT NULL,
#         `user_id` INT UNSIGNED NOT NULL,
#         `created_at` DATETIME NOT NULL,
#         `deleted_at` DATETIME,
#         `deleted` TINYINT NOT NULL,
#         CONSTRAINT `fk_food_user_id` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`))
#     """
# cur.execute(st)
# 購入テーブル作成
st = """
    CREATE TABLE `purchases` (
        `user_id` INT UNSIGNED NOT NULL,
        `food_id` INT UNSIGNED NOT NULL,
        `price` INT UNSIGNED DEFAULT NULL,
　　　　　PRIMARY KEY (`user_id`, `food_id`),
        CONSTRAINT `fk_purchases_user_id` FOREIGN KEY (`user_id`) REFERENCES `users`(`id`),
        CONSTRAINT `fk_purchases_food_id` FOREIGN KEY (`food_id`) REFERENCES `food`(`id`))
    """
cur.execute(st)

# テーブル確認
cur.execute('SELECT * FROM `users`, `food`, `purchases`')
print(cur.fetchall())

# 接続のコミット・クローズ
con.commit()
con.close()
