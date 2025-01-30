from flask import Flask
from flask import request
import time
import datetime

app = Flask(__name__)


@app.route("/")
def home():
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    items = []
    tonow = datetime.datetime.now()
    year = tonow.year
    month = tonow.month
    day = tonow.day
    try:
        with open(f"{year}{month}{day}.txt", "r", encoding="utf-8") as f:
            current_item = ""
            for line in f:
                if "<new/>" in line:
                    items.append(current_item.strip())
                    current_item = ""
                else:
                    current_item += line
            if current_item:
                items.append(current_item.strip())
    except:
        return html.replace("<out/>", "今天還沒有日記。")
    out_arr = "<h2>今天大家的日記<h2/>"
    for i in range(len(items)):
        out_arr += '<div class="diary-entry">'
        out_arr += items[i]
        out_arr += "</div>"
    return html.replace("<out/>", out_arr)


@app.route("/about")
def about():
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    about = ""
    with open("about.html", "r", encoding="utf-8") as f:
        about = f.read()
    return html.replace("<out/>", about)


# @app.route('/signup', methods=['POST'])
@app.route("/signup")
def signup():
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    signup = ""
    with open("signup.html", "r", encoding="utf-8") as f:
        signup = f.read()
    return html.replace("<out/>", signup)


@app.route("/write")
def write():
    html = ""
    writehtml = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    with open("write.html", "r", encoding="utf-8") as f:
        writehtml = f.read()
    return html.replace("<out/>", writehtml)


@app.route("/write_finish", methods=["POST"])
def writefinish():
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    tonow = datetime.datetime.now()
    year = tonow.year
    month = tonow.month
    day = tonow.day
    index = request.form.get("index")
    username = request.form.get("username")
    psw = request.form.get("psw")
    try:
        with open(f"users/{username}.txt", "r", encoding="utf-8") as f:
            pass
    except:
        return html.replace("<out/>", "無此帳號")
    with open(f"users/{username}.txt", "r", encoding="utf-8") as f:
        if psw != f.read():
            return html.replace("<out/>", "密碼不正確")
    with open(f"{year}{month}{day}.txt", "a", encoding="utf-8") as f:
        f.write(index + f"<br> <p>by {username}<p/>")
    return html.replace("<out/>", "日記上傳成功。")


@app.route("/signup_finish", methods=["POST"])
def signupfinish():
    username = request.form.get("username")
    email = request.form.get("email")
    psw1 = request.form.get("psw1")
    psw2 = request.form.get("psw2")
    if psw1 != psw2:
        return "密碼不一致。"
    html = ""
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    try:
        with open(f"users/{username}.txt", "r", encoding="uft-8") as f:
            pass
        return html.replace("<out/>", "已有此username，請更改username。")
    except:
        with open(f"users/{username}.txt", "w", encoding="utf-8") as f:
            f.write(psw1)
    # 尚未測試
    return html.replace("<out/>", "已註冊成功，請再寫文章時登入。")


app.run(debug=True, host="0.0.0.0", port='5100')

"""讀取檔案並且看到<new/>就分割到arr
items = []
with open("alldiary.txt", "r", encoding="utf-8") as f:
    current_item = ""
    for line in f:
        if "<new/>" in line:
            items.append(current_item.strip())
            current_item = ""
        else:
            current_item += line
    if current_item:
        items.append(current_item.strip())
print(items)"""
