from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = 'movie_theatre.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/manager')
def manager():
    conn = get_db()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    return render_template('manager.html', movies=movies)

@app.route('/tickets')
def tickets():
    conn = get_db()
    movies = conn.execute('SELECT * FROM movies').fetchall()
    return render_template('tickets.html', movies=movies)

@app.route('/concessions')
def concessions():
    conn = get_db()
    items = conn.execute('SELECT * FROM concessions').fetchall()
    return render_template('concessions.html', items=items)

@app.route('/add_movie', methods=['POST'])
def add_movie():
    name = request.form['name']
    conn = get_db()
    conn.execute('INSERT INTO movies (name) VALUES (?)', (name,))
    conn.commit()
    return redirect(url_for('manager'))

@app.route('/add_showtime', methods=['POST'])
def add_showtime():
    movie_id = request.form['movie']
    showtime = request.form['showtime']
    conn = get_db()
    conn.execute('INSERT INTO showtimes (movie_id, showtime) VALUES (?, ?)', (movie_id, showtime))
    conn.commit()
    return redirect(url_for('manager'))

@app.route('/change_ticket_prices', methods=['POST'])
def change_ticket_prices():
    movie_id = request.form['movie']
    kid_price = request.form['kid_price']
    adult_price = request.form['adult_price']
    conn = get_db()
    conn.execute('UPDATE movies SET kid_price = ?, adult_price = ? WHERE id = ?', (kid_price, adult_price, movie_id))
    conn.commit()
    return redirect(url_for('manager'))

@app.route('/add_concession_item', methods=['POST'])
def add_concession_item():
    name = request.form['name']
    price = request.form['price']
    conn = get_db()
    conn.execute('INSERT INTO concessions (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    return redirect(url_for('manager'))

@app.route('/sell_tickets', methods=['POST'])
def sell_tickets():
    movie_id = request.form['movie']
    showtime_id = request.form['showtime']
    child_tickets = int(request.form['child_tickets'])
    adult_tickets = int(request.form['adult_tickets'])
    conn = get_db()
    conn.execute('UPDATE showtimes SET remaining_tickets = remaining_tickets - ? WHERE id = ?', (child_tickets + adult_tickets, showtime_id))
    conn.commit()
    return redirect(url_for('tickets'))

@app.route('/refund_tickets', methods=['POST'])
def refund_tickets():
    movie_id = request.form['movie']
    showtime_id = request.form['showtime']
    child_tickets = int(request.form['child_tickets'])
    adult_tickets = int(request.form['adult_tickets'])
    conn = get_db()
    conn.execute('UPDATE showtimes SET remaining_tickets = remaining_tickets + ? WHERE id = ?', (child_tickets + adult_tickets, showtime_id))
    conn.commit()
    return redirect(url_for('tickets'))

@app.route('/get_remaining_tickets', methods=['POST'])
def get_remaining_tickets():
    showtime_id = request.form['showtime']
    conn = get_db()
    remaining_tickets = conn.execute('SELECT remaining_tickets FROM showtimes WHERE id = ?', (showtime_id,)).fetchone()
    return jsonify({'remaining_tickets': remaining_tickets['remaining_tickets']})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
