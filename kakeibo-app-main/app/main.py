from flask import Flask, render_template, request, redirect, Response
import sqlite3
import csv
import io
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute('SELECT * FROM records')
    records = c.fetchall()
    conn.close()
    return render_template('index.html', records=records)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        note = request.form['note']
        conn = sqlite3.connect('kakeibo.db')
        c = conn.cursor()
        c.execute(
            'INSERT INTO records (date, category, amount, note) VALUES (?, ?, ?, ?)',
            (date, category, amount, note)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('add.html')

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute('DELETE FROM records WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
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

@app.route('/export')
def export():
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute('SELECT date, category, amount, note FROM records')
    rows = c.fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['日付', 'カテゴリ', '金額', 'メモ'])  # ヘッダー
    writer.writerows(rows)

    # UTF-8の出力をShift_JISに変換
    sjis_output = output.getvalue().encode('cp932', 'ignore')  # ignoreでエラー>を回避
    return Response(
        sjis_output,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=kakeibo.csv'}
    )

@app.route('/summary')
def summary():
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute('SELECT date, category, amount FROM records')
    records = c.fetchall()
    conn.close()

    summary_data = defaultdict(lambda: {'収入': 0, '支出': 0})

    for date_str, category, amount in records:
        month = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m')
        summary_data[month][category] += amount

    # 月順に並び替え
    summary_sorted = sorted(summary_data.items())

    return render_template('summary.html', summary=summary_sorted)

@app.route('/category_summary')
def category_summary():
    conn = sqlite3.connect('kakeibo.db')
    c = conn.cursor()
    c.execute('SELECT date, category, amount FROM records')
    records = c.fetchall()
    conn.close()

    from collections import defaultdict
    from datetime import datetime

    # 二重の defaultdict
    summary_data = defaultdict(lambda: defaultdict(int))

    for date_str, category, amount in records:
        month = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m')
        summary_data[month][category] += int(amount)

    # 月単位でソート
    summary_sorted = sorted(summary_data.items())

    return render_template('category_summary.html', summary=summary_sorted)

    for date_str, category, amount in records:
        print(f"DEBUG: {date_str=}, {category=}, {amount=}")  # ← 追加
        month = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m')
        summary_data[month][category] += int(amount)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)

