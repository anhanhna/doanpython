import sqlite3
from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

# Hàm kết nối đến cơ sở dữ liệu
def connect_db():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    return conn, cursor

# Route để lưu dữ liệu từ biểu mẫu
@app.route('/api/data', methods=['POST'])
def store_data():
    data = request.json
    
    conn, cursor = connect_db()
    cursor.execute("INSERT INTO products (name, price, quantity) VALUES (?, ?, ?)", (data['name'], data['price'], data['quantity']))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Data stored successfully"})

# Route chính để hiển thị trang chính và danh sách sản phẩm
@app.route('/')
def home():
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    if request.method == 'POST':
        # Lấy dữ liệu từ yêu cầu POST
        id = int(request.form['id'])
        name = request.form['name']
        price = float(request.form['price'])
        quantity = int(request.form['quantity'])

        # Kiểm tra xem sản phẩm đã tồn tại trong cơ sở dữ liệu chưa
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (id,))
        existing_product = cursor.fetchone()
        conn.close()

        if existing_product:
            # Sản phẩm đã tồn tại, tăng số lượng
            new_quantity = existing_product[3] + quantity
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE products SET quantity = ? WHERE id = ?', (new_quantity, id))
            conn.commit()
            conn.close()
            return jsonify({"message": "Quantity increased successfully"})
        else:
            # Sản phẩm chưa tồn tại, thêm hàng mới
            conn = sqlite3.connect('my_database.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (id, name, price, quantity) VALUES (?, ?, ?, ?)', (id, name, price, quantity))
            conn.commit()
            conn.close()
                
            return jsonify({"message": "Data received successfully"})
    
    return redirect(url_for('index'))


# Route để xóa sản phẩm
@app.route('/delete/<int:id>', methods=['POST'])
def delete_product(id):
    conn, cursor = connect_db()
    cursor.execute('DELETE FROM products WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product deleted successfully"})

# Route để kiểm tra sự trùng lặp dựa trên ID và tên
@app.route('/check_duplicate', methods=['POST'])
def check_duplicate():
    data = request.json
    id = data['id']
    name = data['name']
    
    conn, cursor = connect_db()
    cursor.execute('SELECT * FROM products WHERE id=? AND name=?', (id, name))
    product = cursor.fetchone()
    conn.close()
    
    duplicate = False
    matching_name = False
    
    if product:
        duplicate = True
        matching_name = True
    
    return jsonify({"duplicate": duplicate, "matchingName": matching_name})

# Route để tăng số lượng của sản phẩm đã tồn tại
@app.route('/increase_quantity/<int:id>', methods=['POST'])
def increase_quantity(id):
    data = request.json
    quantity = data['quantity']
    
    conn, cursor = connect_db()
    cursor.execute('UPDATE products SET quantity=quantity+? WHERE id=?', (quantity, id))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Quantity increased successfully"})

# Route để tự động điền Name và Price khi nhập ID
@app.route('/get_product_info/<int:id>', methods=['GET'])
def get_product_info(id):
    conn, cursor = connect_db()
    cursor.execute('SELECT name, price FROM products WHERE id=?', (id,))
    product_info = cursor.fetchone()
    conn.close()

    if product_info:
        return jsonify({"id": id, "name": product_info[0], "price": product_info[1]})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
