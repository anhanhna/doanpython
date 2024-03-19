import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify

app = Flask(__name__)

# Kết nối đến cơ sở dữ liệu (hoặc tạo cơ sở dữ liệu mới nếu chưa tồn tại)
conn = sqlite3.connect('my_database.db')

# Tạo một đối tượng Cursor để thực hiện các truy vấn SQL
cursor = conn.cursor()

# Tạo bảng trong cơ sở dữ liệu
cursor.execute('''CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    number INTEGER NOT NULL
                )''')
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT,
                    number REAL NOT NULL
                )''')
# Lưu các thay đổi và đóng kết nối đến cơ sở dữ liệu
conn.commit()
conn.close()

@app.route('/api/data', methods=['POST'])
def store_data():
    data = request.json
    
    # Kết nối đến cơ sở dữ liệu SQLite
    conn = sqlite3.connect('my_database.db')
    
    cursor = conn.cursor()
    
    # Thêm dữ liệu vào bảng
    cursor.execute("INSERT INTO products (name, price, number) VALUES (?, ?, ?)", (data['name'], data['price'], data['number']))
    
    # Lưu thay đổi và đóng kết nối
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Data stored successfully"})

@app.route('/')
def home():
    # Truy vấn tất cả sản phẩm từ cơ sở dữ liệu và hiển thị trên trang
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Lấy dữ liệu từ yêu cầu POST
        name = request.form['name']
        price = request.form['price']
        number = request.form['number']
        
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO products (name, price, number) VALUES (?, ?, ?)', (name, price, number))  # Sửa lỗi ở đây
        conn.commit()
        conn.close()
        return jsonify({"message": "Data received successfully"})
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

