
from flask import Flask, render_template, request, redirect
from models import db, Product

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    description = request.form['description']
    price = float(request.form['price'])
    seller = request.form['seller']  # Ethereum адрес продавца
    image_url = request.form['image_url']

    new_product = Product(name=name, description=description, price=price, seller=seller, image_url=image_url)
    db.session.add(new_product)
    db.session.commit()

    return redirect('/')


if _name_ == '_main_':
    app.run(debug=True)

    python
    from flask import Flask, render_template, request, redirect, url_for, session
    from models import db, Product, CartItem

    app = Flask(_name_)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
    app.secret_key = 'your_secret_key'  # Необходимо для использования сессий
    db.init_app(app)

    with app.app_context():
        db.create_all()


    @app.route('/')
    def index():
        products = Product.query.all()
        return render_template('index.html', products=products)


    @app.route('/add_product', methods=['POST'])
    def add_product():
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        seller = request.form['seller']
        image_url = request.form['image_url']

        new_product = Product(name=name, description=description, price=price, seller=seller, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()

        return redirect('/')


    @app.route('/add_to_cart/<int:product_id>')
    def add_to_cart(product_id):
        if 'cart' not in session:
            session['cart'] = {}

        if str(product_id) in session['cart']:
            session['cart'][str(product_id)] += 1
        else:
            session['cart'][str(product_id)] = 1

        return redirect('/')


    @app.route('/cart')
    def cart():
        if 'cart' not in session:
            session['cart'] = {}

        cart_items = []
        total_price = 0
        for product_id, quantity in session['cart'].items():
            product = Product.query.get(int(product_id))
            if product:
                cart_items.append({'product': product, 'quantity': quantity})
                total_price += product.price * quantity

        return render_template('cart.html', cart_items=cart_items, total_price=total_price)


    @app.route('/checkout')
    def checkout():
        # Здесь можно добавить логику оформления заказов
        session.pop('cart', None)  # Очищение корзины после оформления
        return redirect('/')


    if _name_ == '_main_':
        app.run(debug=True)
        python
        from flask import Flask, render_template, request, redirect, session, jsonify
        from tonclient import TonClient, DevNet
        from models import db, Product, CartItem

        app = Flask(_name_)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
        app.secret_key = 'your_secret_key'
        db.init_app(app)

        with app.app_context():
            db.create_all()
client = TonClient(network=DevNet())
python
@app.route('/pay', methods=['POST'])
def pay():
    # Получаем данные платежа (например, адрес и сумму)
    data = request.json
    amount = data.get('amount')
    recipient = data.get('recipient')
  return jsonify({'status': 'Payment processed successfully!'})

python
import requests
from flask import Flask, render_template, request, redirect, session, jsonify

# Конфигурация
MIR_URL = "https://api.mironline.ru/..."  # Укажите ваш URL для API системы "Мир"
MERCHANT_ID = "YOUR_MERCHANT_ID"
SECRET_KEY = "YOUR_SECRET_KEY"

app = Flask(_name_)
app.secret_key = 'your_secret_key'

# Ваши другие конфигурации...

@app.route('/pay_mir', methods=['POST'])
def pay_mir():
    amount = request.json.get('amount')  # Сумма в копейках
    order_id = request.json.get('order_id')  # Уникальный идентификатор заказа
    description = "Payment for order #" + order_id

    payload = {
        "merchantId": MERCHANT_ID,
        "amount": amount,
        "currency": "RUB",
        "orderId": order_id,
        "description": description,
        # Другие параметры API, если требуется
    }

    # Генерация подписи (в этом примере это просто текст, в реальной ситуации используйте хеширование)
    signature = generate_signature(payload, SECRET_KEY)
    payload['signature'] = signature

    response = requests.post(MIR_URL, json=payload)

    if response.status_code == 200:
        # Обработка успешного платежа
        return jsonify({"status": "success", "data": response.json()})
    else:
        # Обработка ошибок
        return jsonify({"status": "error", "message": response.text}), response.status_code

def generate_signature(data, secret):
    # Ваш код для генерации подписи (например, используя hashlib)
    import hashlib
    sorted_data = sorted(data.items())
    sign_string = ''.join(f'{key}={value}' for key, value in sorted_data) + secret
    return hashlib.sha256(sign_string.encode()).hexdigest()
