from flask import Flask
import webbrowser

app = Flask(__name__)

@app.route("/")
def white_page():
    return "こんにちは <h1>トップページ</h1>"
    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run()





"""from flask import Flask
import webbrowser

app = Flask(__name__)

@app.route("/")
def white_page():
    return "こんにちは <h1>トップページ</h1>"
    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run()
""" 
"""  
♯ターミナルで→を入力しflaskをインストール。　python3 -m pip install flask
♯出てきたhttp127.~5000をアドレスバーに貼り付ければOK。
♯5000番という空き地にflaskという建物（工場）がある。どういう商品を作るかの製造ライン（関数）は無いのでdefで作りreturnで表示させる。
import webbrowser
webbrowser.open("http://127.0.0.1:5000")　この2文でF5押したら更新されたページ出てくる。
出ないならpythonを一回終了させてF5を試そう。もしくはhttp://127.0.0.1:5000を入力。
shift+3でコメントアウト。ハッシュという。シャープ♯では無い。
F5押すと更新のたびに新たなタブ出るが我慢して。リロードだけのは難しい。
"""

"""password="1234"
input_pw=input("パスワード入力してね")

if input_pw==password:
    print("ログインしました")
else:
    print("ログイン失敗")
♯1234も文字列"1234"にしないと何の数字入れてもログイン失敗が表示される。
"""

"""import os
os.system("open -a Notes.app")
→finder アプリケーション 右クリック 情報を見る　名前と拡張子で正式なアプリ名見れる
"""

"""import os
os.system("open -a Launchpad")
"""

"""
chars="abcdefghijk"
for i in range(11):
    print(chars[i])
"""


"""
single=True
married=False

a=single
b=married

if a==True:
    print("あなたは独身")
else:
    print("あなたは既婚者")
"""


"""
income = 500
single= True

if income>= 1000:
    tax=0.1*income
    tedori=income-tax
    print(f"収入{income}円:独身のため{tax}円増税のため手取り{tedori}円です")
else:
    tax2=1.1*income
    tedori=income+tax2
    print(f"収入{income}円:独身のため{tax2}円増税のため手取り{tedori}円です")
"""


"""
a=1001
if a>1000:
    print("今日は100円の給料だ")
else:
    print("今日は節約だ")
"""


"""
import tkinter as tk

def send(event=None):
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("フォーム")

entry = tk.Entry(root)
entry.pack()

# Enterキーと関数を紐づける
entry.bind("<Return>", send)

root.mainloop()
"""



"""
while True:
    str=input("名前を入力してください(qを押すと終了になります)")
    if str=="q":
        break
    print(str,"が入力されました")
"""
