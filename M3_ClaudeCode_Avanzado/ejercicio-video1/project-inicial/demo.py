from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('rebel_ops.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/health', methods=['GET'])
def get_health():
    db = get_db()
    count = db.execute('SELECT COUNT(*) FROM missions').fetchone()[0]
    return jsonify({'data': {'status': 'ok', 'missions': count}, 'error': None})

@app.route('/missions', methods=['GET'])
def get_missions():
    db = get_db()
    missions = db.execute('SELECT * FROM missions').fetchall()
    return jsonify({'data': [dict(m) for m in missions], 'error': None})

@app.route('/missions', methods=['POST'])
def post_mission():
    body = request.get_json()
    if not body or 'name' not in body:
        return jsonify({'data': None, 'error': 'name requerido'}), 400
    db = get_db()
    db.execute('INSERT INTO missions (name) VALUES (?)', (body['name'],))
    db.commit()
    return jsonify({'data': {'created': True}, 'error': None}), 201

if __name__ == '__main__':
    app.run(debug=True, port=5000)
