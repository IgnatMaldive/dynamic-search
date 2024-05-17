from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def query_db(query, args=(), one=False):
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    if query:
        sql_query = f"SELECT * FROM data WHERE {' OR '.join([f'{col} LIKE ?' for col in get_columns()])}"
        args = [f'%{query}%'] * len(get_columns())
        results = query_db(sql_query, args)
    else:
        results = query_db("SELECT * FROM data")
    return jsonify([dict(row) for row in results])

def get_columns():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    cur.execute('PRAGMA table_info(data)')
    columns = [info[1] for info in cur.fetchall()]
    cur.close()
    conn.close()
    return columns

if __name__ == '__main__':
    app.run(debug=True, port=5002)
