from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
from pathlib import Path

app = Flask(__name__)

# 受注データを保存するJSONファイルのパス
ORDERS_FILE = Path('orders.json')

def load_orders():
    """JSONファイルから受注データを読み込む"""
    if ORDERS_FILE.exists():
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_orders(orders):
    """受注データをJSONファイルに保存"""
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    """受注フォームページ"""
    return render_template('受注フォーム')

@app.route('/submit', methods=['POST'])
def submit():
    """フォーム送信処理"""
    orders = load_orders()
    
    new_order = {
        'id': len(orders) + 1,
        'patient': request.form.get('patient'),
        'drug_name': request.form.get('drug_name'),
        'quantity': int(request.form.get('quantity')),
        'date': request.form.get('date'),
        'submitted_at': datetime.now().isoformat()
    }
    
    orders.append(new_order)
    save_orders(orders)
    
    return redirect(url_for('orders_list'))

@app.route('/orders_list')
def orders_list():
    """受注一覧ページ"""
    orders = load_orders()
    return render_template('orders_list.html', orders=orders)

if __name__ == '__main__':
    app.run(debug=True)
