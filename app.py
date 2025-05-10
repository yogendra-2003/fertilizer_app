from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database initialization
def init_db():
    conn = sqlite3.connect('fertilizers.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fertilizers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Home Page (User view)
@app.route('/')
def home():
    conn = sqlite3.connect('fertilizers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fertilizers')
    fertilizers = cursor.fetchall()
    conn.close()
    return render_template('home.html', fertilizers=fertilizers)

# Add to cart
@app.route('/add_to_cart/<int:fertilizer_id>')
def add_to_cart(fertilizer_id):
    cart = session.get('cart', [])
    cart.append(fertilizer_id)
    session['cart'] = cart
    return redirect(url_for('home'))

# View cart
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    conn = sqlite3.connect('fertilizers.db')
    cursor = conn.cursor()
    items = []
    total = 0
    for fid in cart:
        cursor.execute('SELECT * FROM fertilizers WHERE id = ?', (fid,))
        item = cursor.fetchone()
        if item:
            items.append(item)
            total += item[2]
    conn.close()
    return render_template('cart.html', items=items, total=total)

# Admin dashboard
@app.route('/admin')
def admin():
    conn = sqlite3.connect('fertilizers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM fertilizers')
    fertilizers = cursor.fetchall()
    conn.close()
    return render_template('admin.html', fertilizers=fertilizers)

# Add fertilizer (admin)
@app.route('/admin/add', methods=['GET', 'POST'])
def add_fertilizer():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        conn = sqlite3.connect('fertilizers.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO fertilizers (name, price, description) VALUES (?, ?, ?)',
                       (name, price, description))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))
    return render_template('add_fertilizer.html')

# Edit fertilizer (admin)
@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit_fertilizer(id):
    # This is for edit fertlizer
    conn = sqlite3.connect('fertilizers.db')
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        cursor.execute('UPDATE fertilizers SET name=?, price=?, description=? WHERE id=?',
                       (name, price, description, id))
        conn.commit()
        conn.close()
        return redirect(url_for('admin'))

    cursor.execute('SELECT * FROM fertilizers WHERE id = ?', (id,))
    fertilizer = cursor.fetchone()
    conn.close()
    return render_template('edit_fertilizer.html', fertilizer=fertilizer)

# Delete fertilizer (admin)
@app.route('/admin/delete/<int:id>')
def delete_fertilizer(id):
    conn = sqlite3.connect('fertilizers.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fertilizers WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
