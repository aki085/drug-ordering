from flask import Flask, render_template, request, Response
import sqlite3
import os
import csv
from io import StringIO

app = Flask(__name__)
DB = 'orders.db'

# --------------------
# DB初期化
# --------------------
def init_db():
    with sqlite3.connect(DB, timeout=10) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS drugs (
                drug_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id INTEGER,
                order_date TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
            )
        ''')
        c.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                drug_id INTEGER,
                quantity INTEGER,
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (drug_id) REFERENCES drugs(drug_id)
            )
        ''')

init_db()

# --------------------
# トップページ（受注フォーム）
# --------------------
@app.route('/')
def index():
    return render_template('index.html')

# --------------------
# 受注フォーム送信
# --------------------
@app.route('/submit', methods=['POST'])
def submit():
    patient_name = request.form['patient'].strip()
    drug_name = request.form['drug_name'].strip()
    try:
        quantity = int(request.form['quantity'])
    except ValueError:
        return "数量は数字で入力してください"
    order_date = request.form['date']

    try:
        with sqlite3.connect(DB, timeout=10) as conn:
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO patients (name) VALUES (?)", (patient_name,))
            c.execute("SELECT patient_id FROM patients WHERE name = ?", (patient_name,))
            patient_id = c.fetchone()[0]

            c.execute("INSERT OR IGNORE INTO drugs (name) VALUES (?)", (drug_name,))
            c.execute("SELECT drug_id FROM drugs WHERE name = ?", (drug_name,))
            drug_id = c.fetchone()[0]

            c.execute("INSERT INTO orders (patient_id, order_date) VALUES (?, ?)", (patient_id, order_date))
            order_id = c.lastrowid

            c.execute("INSERT INTO order_items (order_id, drug_id, quantity) VALUES (?, ?, ?)",
                      (order_id, drug_id, quantity))
    except sqlite3.OperationalError as e:
        return f"データベースエラーが発生しました: {e}"

    return "受注をデータベースに保存しました！"

# --------------------
# 受注一覧ページ
# --------------------
@app.route('/orders')
def orders_list():
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT o.order_id, p.name, d.name, oi.quantity, o.order_date
            FROM orders o
            LEFT JOIN patients p ON o.patient_id = p.patient_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            LEFT JOIN drugs d ON oi.drug_id = d.drug_id
            ORDER BY o.order_id DESC
        ''')
        orders = c.fetchall()
    return render_template('order.html', orders=orders)

@app.route('/edit/<int:order_id>', methods=['GET', 'POST'])
def edit_order(order_id):

    # 更新ボタンを押した場合
    if request.method == 'POST':

        patient_name = request.form['patient'].strip()
        drug_name = request.form['drug_name'].strip()
        quantity = int(request.form['quantity'])
        order_date = request.form['date']

        with sqlite3.connect(DB) as conn:
            c = conn.cursor()

            # 患者名更新
            c.execute("""
                UPDATE patients
                SET name = ?
                WHERE patient_id = (
                    SELECT patient_id
                    FROM orders
                    WHERE order_id = ?
                )
            """, (patient_name, order_id))


            # 薬品名更新
            c.execute("""
                UPDATE drugs
                SET name = ?
                WHERE drug_id = (
                    SELECT drug_id
                    FROM order_items
                    WHERE order_id = ?
                )
            """, (drug_name, order_id))


            # 数量更新
            c.execute("""
                UPDATE order_items
                SET quantity = ?
                WHERE order_id = ?
            """, (quantity, order_id))


            # 注文日更新
            c.execute("""
                UPDATE orders
                SET order_date = ?
                WHERE order_id = ?
            """, (order_date, order_id))


        return "<script>window.location.href='/orders';</script>"


    # 編集画面を開いた場合（GET）
    with sqlite3.connect(DB) as conn:
        c = conn.cursor()

        c.execute("""
            SELECT
                o.order_id,
                p.name,
                d.name,
                oi.quantity,
                o.order_date
            FROM orders o
            LEFT JOIN patients p
                ON o.patient_id = p.patient_id
            LEFT JOIN order_items oi
                ON o.order_id = oi.order_id
            LEFT JOIN drugs d
                ON oi.drug_id = d.drug_id
            WHERE o.order_id = ?
        """, (order_id,))

        order = c.fetchone()


    return render_template('edit.html', order=order)
    



# --------------------
# 注文削除
# --------------------
@app.route('/delete/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    try:
        with sqlite3.connect(DB, timeout=10) as conn:
            c = conn.cursor()
            c.execute("DELETE FROM order_items WHERE order_id = ?", (order_id,))
            c.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
    except sqlite3.OperationalError as e:
        return f"データベースエラーが発生しました: {e}"
    return "<script>window.location.href='/orders';</script>"

# --------------------
# CSV出力（OS対応）
# クエリパラメータ ?os=windows または ?os=mac
# --------------------
@app.route('/export_csv')
def export_csv():
    os_type = request.args.get('os', 'mac').lower()  # デフォルトは mac (UTF-8)
    encoding = 'cp932' if os_type == 'windows' else 'utf-8'

    with sqlite3.connect(DB) as conn:
        c = conn.cursor()
        c.execute('''
            SELECT o.order_id, p.name, d.name, oi.quantity, o.order_date
            FROM orders o
            LEFT JOIN patients p ON o.patient_id = p.patient_id
            LEFT JOIN order_items oi ON o.order_id = oi.order_id
            LEFT JOIN drugs d ON oi.drug_id = d.drug_id
            ORDER BY o.order_id DESC
        ''')
        orders = c.fetchall()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['注文ID', '患者名', '薬品名', '数量', '注文日'])
    for o in orders:
        writer.writerow(o)

    output = si.getvalue().encode(encoding, 'replace')

    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition":"attachment;filename=orders.csv"}
    )

# --------------------
# アプリ起動
# --------------------
if __name__ == "__main__":
    app.run(debug=True)

