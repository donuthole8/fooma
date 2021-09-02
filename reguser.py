from flask_bcrypt import Bcrypt
import re
import data

def check_mail(msg, mail):
    """
    メールアドレスのバリデーション
    param mail: メールアドレス
    """

    # メールの存在角煮
    if len(mail) == 0:
        msg.append("メールアドレスを入力して下さい")

    # メールのフォーマット確認
    pattern = "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not (re.match(pattern, mail)):
        msg.append("正しいメールアドレスを入力して下さい")

    # メールの文字数確認（128文字）
    print(len(mail))
    if len(mail) > 128:
        msg.append("メールアドレスは128文字以内で入力して下さい")

    # メールの一意性チェック
    if (data.check_duplication(mail)):
        msg.append("既に存在するメールアドレスです")

    # エラーがなければTrueを返却
    return msg, (msg==[])


def check_pass(msg, pw):
    """
    パスワードのバリデーション
    param pw: パスワード
    """

    # パスワードの存在確認
    if (len(pw) == 0):
        msg.append("パスワードを入力して下さい")

    # パスワードの文字数確認
    if (len(pw) > 30):
        msg.append("パスワードは30文字以内で入力して下さい")

    # エラーメッセージが無ければTrueを返却
    return msg, (msg==[])


def check_pass_match(msg, pw, pw_check):
    """
    再入力パスワードとパスワードの一致確認
    param pw: パスワード
    param pw_check: 再入力パスワード
    """

    # 一致確認
    if (pw != pw_check):
        msg.append("確認用パスワードが違います")

    # エラーメッセージが無ければTrueを返却
    return msg, (msg==[])


def encryption(pw):
    """
    パスワードの暗号化
    param pw: パスワード
    """

    # bcryptによるハッシュ化
    bcrypt = Bcrypt()
    enc_pw = bcrypt.generate_password_hash(pw)
    print(enc_pw)

    # ハッシュ値を返却
    return enc_pw


def validation(mail, pw, pw_check):
    """
    バリデーション
    param mail: メールアドレス
    param pw: パスワード
    param pw_check: 再入力パスワード
    """

    # エラーメッセージ
    msg = []

    # メールアドレスのバリデーション
    msg,isCorrect = check_mail(msg, mail)

    # パスワードのバリデーション
    msg,isCorrect = check_pass(msg, pw)

    # 再入力パスワードの確認
    msg,isCorrect = check_pass_match(msg, pw, pw_check)

    # エラーがある場合Falseを返却
    if not isCorrect:
        return msg, False

    # パスワードの暗号化
    enc_pw = encryption(pw)

    # データベースへの追加
    data.add_regdata(mail, enc_pw)

    # Trueを返却
    return msg, True

