from flask import Flask, render_template, request, redirect, Response
import sqlite3
import csv
import io
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# --- DB 接続共通関数 ---
def get_db_connection():
    conn = sqlite3.connect('kakeibo.db')
    conn.row_factory = sqlite3.Row  # 行で取り出す時に便利
    return conn


# --- 一覧表示 ---
@app.route('/')
def index():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM records')
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)


# --- 登録 ---
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = int(request.form['amount'])
        note = request.form['note']
        conn = get_db_connection()
        c = conn.cursor()
        c.execute(
            'INSERT INTO records (date, category, amount, note) VALUES (?, ?, ?, ?)',
            (date, category, amount, note)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')


# --- 編集 ---
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    c = conn.cursor()
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = int(request.form['amount'])
        note = request.form['note']
        c.execute(
            'UPDATE records SET date = ?, category = ?, amount = ?, note = ? WHERE id = ?',
            (date, category, amount, note, id)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        c.execute('SELECT * FROM records WHERE id = ?', (id,))
        record = c.fetchone()
        conn.close()
        return render_template('edit.html', record=record)


# --- 削除 ---
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


# --- CSV エクスポート ---
@app.route('/export')
def export():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT date, category, amount, note FROM records')
    rows = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['日付', 'カテゴリ', '金額', 'メモ'])
    for row in rows:
        writer.writerow([row['date'], row['category'], row['amount'], row['note']])

    utf8_output = output.getvalue().encode('utf-8-sig')  # Excel互換
    return Response(
        utf8_output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=kakeibo.csv'}
    )


# --- 月別収支サマリ ---
@app.route('/summary')
def summary():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT date, category, amount FROM records')
    records = c.fetchall()
    conn.close()

    summary_data = defaultdict(lambda: defaultdict(int))

    for row in records:
        month = datetime.strptime(row['date'], '%Y-%m-%d').strftime('%Y-%m')
        category = row['category']
        amount = int(row['amount'])
        summary_data[month][category] += amount

    summary_sorted = sorted(summary_data.items())
    return render_template('summary.html', summary=summary_sorted)


# --- カテゴリ別サマリ ---
@app.route('/category_summary')
def category_summary():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT date, category, amount FROM records')
    records = c.fetchall()
    conn.close()

    summary_data = defaultdict(lambda: defaultdict(int))

    for row in records:
        month = datetime.strptime(row['date'], '%Y-%m-%d').strftime('%Y-%m')
        category = row['category']
        amount = int(row['amount'])
        summary_data[month][category] += amount

    summary_sorted = sorted(summary_data.items())
    return render_template('category_summary.html', summary=summary_sorted)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
