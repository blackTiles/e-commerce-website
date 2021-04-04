from flask import Flask, render_template, request, redirect, jsonify, flash, session
import base64
import os
import string
import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.sqlite'
db = SQLAlchemy(app)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(100))
    image_name = db.Column(db.String(300))
    image_data = db.Column(db.LargeBinary)
    description = db.Column(db.String(300))
    price = db.Column(db.String(10))

class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    user_name = db.Column(db.String(100))
    email = db.Column(db.String(150))  
    password = db.Column(db.String(50))
    last_otp = db.Column(db.String(8))
    is_verified = db.Column(db.Integer)

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True) 
    product_id = db.Column(db.Integer)
    _user_id = db.Column(db.Integer)

class Orders(db.Model):
    order_id = db.Column(db.Integer, primary_key=True) 
    id_of_user = db.Column(db.Integer)
    name_of_items = db.Column(db.String(300))
    full_address = db.Column(db.String(500))
    total_price = db.Column(db.String(10))
    order_date = db.Column(db.String(30))

@app.route('/')
def main():
    if 'userid' in session:
        user_query = Users.query.filter_by(id=session['userid']).first()
        if user_query.is_verified:
            user_data = [user_query.id, user_query.user_name, user_query.email]

            products_data_database = Products.query.all()
            list_of_products_data = []
            
            for x in products_data_database:
                products_data = []
                data = base64.b64encode(x.image_data)
                data = data.decode("UTF-8")
                products_data.append(x.id)
                products_data.append(data)
                products_data.append(x.category)
                products_data.append(x.description)
                products_data.append(x.price)
                list_of_products_data.append(products_data)
            return render_template('login.html', session_user_data=[user_data[0],user_data[1],list_of_products_data, user_data[2]])
        else:
            return redirect('/verify_email')
    else:
        return render_template('index.html')

@app.route('/products')
def products():
    if 'userid' in session:
        return redirect('/')
    else:
        products_data_database = Products.query.all()
        list_of_products_data = []
        
        for x in products_data_database:
            products_data = []
            data = base64.b64encode(x.image_data)
            data = data.decode("UTF-8")
            products_data.append(x.id)
            products_data.append(data)
            products_data.append(x.category)
            products_data.append(x.description)
            products_data.append(x.price)
            list_of_products_data.append(products_data)
        return render_template("products.html", data_list=list_of_products_data)


admin_key = []

@app.route('/validate', methods=['POST', 'GET'])
def validate():
    admin_verified = '1'
    if request.method=='POST':
        pass_key = request.form['passkey']
        if pass_key != '':
            if pass_key == '4766':
                admin_key.append(1)
                return redirect('/admin')
            else:
                return redirect('/')
        return redirect('/')
    else:
        return redirect('/')


@app.route('/admin')
def admin():
    if len(admin_key) > 0:
        return render_template('admin.html')
    else:
        return redirect('/')

@app.route('/admin_logout')
def admin_logout():
    if len(admin_key) == 0:
        return redirect('/') 
    else:
        admin_key.pop(0)
        return redirect('/admin')

@app.route('/upload', methods=['POST'])
def upload():
    category = request.form['category']
    file = request.files['filename']
    desc = request.form['description']
    price = request.form['price']
    newProduct = Products(category = category, image_name=file.filename, image_data = file.read(), description=desc, price= price)
    db.session.add(newProduct)
    db.session.commit()
    flash('Product inserted into the database')
    return redirect('/admin')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        l_email = request.form['inputEmail']
        l_pass = request.form['inputPass']
        if not l_email or not l_pass:
            return jsonify({'error':'Input field is empty'})
        else:
            user_query = Users.query.filter_by(email=l_email, password=l_pass).first()
            if user_query:
                user_data = [user_query.id, user_query.user_name, user_query.email]
                session['userid'] = user_data[0]
                return redirect('/')
            else:
                return jsonify({'notExist':'User not Found'})
    else:
        return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_name = request.form['signUser']
        email = request.form['signEmail']
        password = request.form['signPass']
        if not user_name or not email or not password:
            return jsonify({'error':'Missing Data!'})
        else:
            check_if_already = Users.query.filter_by(email = email).first()
            if check_if_already:
                return jsonify({'alreadyExist':'Email already registered'})
            else:
                otp = str(''.join(random.choice(string.digits) for i in range(6)))
                newUser = Users(user_name = user_name, email = email, password = password, last_otp = otp)
                db.session.add(newUser)
                db.session.commit()
                user_query = Users.query.filter_by(email=email, password=password).first()
                user_data = [user_query.id, user_query.user_name, user_query.email]
                session['userid'] = user_data[0]
                # send otp 
                sender_email = "black4tiles@gmail.com"
                receiver_email = user_data[2]
                password = "piastrellenere?mean4805"
                message = MIMEMultipart("alternative")
                message["Subject"] = "OTP verification"
                message["From"] = sender_email
                message["To"] = receiver_email
                html = """\
                        <html>
                        <head>
                        <meta charset="UTF-8">
                        <meta http-equiv="X-UA-Compatible" content="IE=edge">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        </head>
                        <body>
                            <div style="align-items:center;">
                                <div style="margin:0px auto;text-align:center;"><img src="https://scontent.fdbd1-1.fna.fbcdn.net/v/t1.6435-9/p843x403/149769738_232347528522986_2842490704685962839_n.jpg?_nc_cat=104&ccb=1-3&_nc_sid=730e14&_nc_ohc=eNwNq40XRIgAX_HUntj&_nc_ht=scontent.fdbd1-1.fna&tp=6&oh=ad32f5ab2e09047e398281762a9fd502&oe=608EAA61" width="100" height="100" /></div>
                                <br />
                                <h1 style="font-family:sans-serif; color:grey;text-align:center;">Email Confirmation OTP</h1>
                                <br />
                                <h1 style="font-family:sans-serif; padding:10px; border: 2px dashed black;text-align:center;">{}</h1>
                                <br />
                                <p style="text-align:center">Thank you for being a member of black tiles</p>
                                <hr />
                            </div>
                        </body>
                        </html>
                        """.format(otp)
                part1 = MIMEText(html, "html")
                message.attach(part1)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
                return jsonify({'verify':'/verify_email'})
    else:
        return redirect('/')

@app.route('/verify_email')
def verify_email():
    if 'userid' in session:
        check_if_verified = Users.query.filter_by(id=session['userid']).first()
        if check_if_verified.is_verified:
            return redirect('/')
        else:
            return render_template('verifyotp.html',user_mail = check_if_verified.email)
    else:
        return redirect('/')

@app.route('/confirm_otp', methods=['POST'])
def confirm_otp():
    if 'userid' in session:
        if request.method=='POST':
            input_otp = request.form['otp']
            check_otp = Users.query.filter_by(id=session['userid']).first()
            if check_otp.last_otp==input_otp:
                check_otp.is_verified=1
                db.session.commit()
                return redirect('/')
            else:
                return redirect('/verify_email')
    else:
        return redirect('/')

@app.route('/cancel_and_delete')
def cancel_and_delete():
    if 'userid' in session:
        usr_to_del = Users.query.filter_by(id=session['userid']).first()
        db.session.delete(usr_to_del)
        db.session.commit()
        session.pop('userid',None)
        return redirect('/')
    else:
        return redirect('/')

@app.route('/logout/<id>')
def logout(id):
    if 'userid' in session:
        session.pop('userid',None)
        return redirect('/')
    else:
        return redirect('/')

@app.route('/cart/<usr_id>')
def cart(usr_id):
    if 'userid' in session:
        fetchCartData = Cart.query.filter_by(_user_id=usr_id).all()
        per_list = []
        for m in fetchCartData:
            temp_list = []
            fetchProductData = Products.query.filter_by(id=m.product_id).first()
            data = base64.b64encode(fetchProductData.image_data)
            data = data.decode("UTF-8")
            temp_list.append(fetchProductData.id)
            temp_list.append(data)
            temp_list.append(fetchProductData.category)
            temp_list.append(fetchProductData.description)
            temp_list.append(fetchProductData.price)
            per_list.append(temp_list)
        total_price = 0
        for tp in per_list:
            total_price+=int(tp[4])
        
        return render_template("cart.html", cart_list=[per_list,session['userid'], str(total_price)])
    else:
        return redirect('/')

@app.route('/addToCart', methods=['POST'])
def addTo():
    if 'userid' in session:
        add_to_cart = Cart(_user_id = session['userid'], product_id= request.form['productId'])
        db.session.add(add_to_cart)
        db.session.commit()
        return jsonify({'success':'Item Added'})
    else:
        return redirect('/')

@app.route('/dropFromCart', methods=['POST'])
def dropFromCart():
    if 'userid' in session:
        obj = Cart.query.filter_by(_user_id=session['userid'], product_id=request.form['itemId']).first()
        db.session.delete(obj)
        db.session.commit()
        total_price = 0
        getFromCart = Cart.query.filter_by(_user_id=session['userid']).all()
        for p in getFromCart:
            getPriceFromProduct = Products.query.filter_by(id=p.product_id).first()
            total_price+=int(getPriceFromProduct.price)
        return jsonify({'success':'Item removed from Cart', 'price':str(total_price)})
    else:
        return redirect('/')



@app.route('/confirm_the_order', methods=['POST','GET'])
def confirm_the_order():
    if request.method=='POST':
        full_name = request.form['full_name']
        phone_number = request.form['phone_number']
        address1 = request.form['address1']
        address2 = request.form['address2']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        if not full_name or not phone_number or not address1 or not city or not state:
            return redirect("/cart/{}".format(session['userid']))
        else:
            fetchCartData_ = Cart.query.filter_by(_user_id=session['userid']).all()
            desc = []
            full_description = "+"
            price_of_items = 0
            for k in fetchCartData_:
                fetchProductData_ = Products.query.filter_by(id=k.product_id).first()
                desc.append(str(fetchProductData_.description))
                price_of_items+=int(fetchProductData_.price)
            full_description=full_description.join(desc)
            full_address = f"{full_name}\n Phone No.({phone_number})\n{address2},{address1}\n{city},{state}\n{zip_code}"
            x = datetime.now()
            db.session.add(Orders(id_of_user=session['userid'], name_of_items = full_description, full_address=full_address, total_price=price_of_items, order_date = x.strftime("%d %b, %Y")))
            db.session.commit()
            obj_clear = Cart.query.filter_by(_user_id=session['userid']).all()
            for o in obj_clear:
                db.session.delete(o)
                db.session.commit()
            return redirect("/orders/{}".format(session['userid']))
    else:
        return redirect('/')

@app.route('/orders/<usrid>')
def orders(usrid):
    if 'userid' in session:
        fetch_from_orders = Orders.query.filter_by(id_of_user=session['userid']).all()
        return render_template('orders.html', order = fetch_from_orders)
    else:
        return redirect('/')

@app.route('/cancelOrder', methods=['POST'])
def cancelOrder():
    if 'userid' in session:
        db.session.delete(Orders.query.filter_by(order_id=request.form['_orderID']).first())
        db.session.commit()
        return jsonify({'success':'Order has been Cancelled'})
    else:
        return redirect('/')


@app.route('/update_profile', methods=['POST'])
def update_profile():
    if request.method=='POST':
        u_name = request.form['user_name']
        u_email = request.form['user_email']
        if u_name and u_email:
            get_user_data = Users.query.filter_by(id=session['userid']).first()
            get_user_data.user_name=u_name
            db.session.commit()
            get_user_data.email=u_email
            db.session.commit()
            return jsonify({'success':'Updated Successfully!','username':u_name})         
        else:
            return jsonify({'error':'Missing Data'})
    else:
        return redirect('/')

@app.route("/feedback", methods=["POST","GET"])
def feedback():
    if request.method == "POST":
        sender_name = request.form['sender_name']
        sender_email = request.form['sender_email']
        sender_msg = request.form['sender_msg']
        if not sender_msg:
            return jsonify({'empty':'Message is missing'})
        else:
            account_sid = 'AC7b7eba1c290afbf3365bc5139e0b956a' 
            auth_token = '997e66e7ae1f9c1242b855ff07137e9e' 
            client = Client(account_sid, auth_token) 
            message = client.messages.create( 
                                        from_='+13212412340',  
                                        body=f'{sender_name}\n{sender_email}\n{sender_msg}',      
                                        to='+917319865341' 
                                    ) 
            return jsonify({'sent':'Message Sent!'})
    else:
        return redirect("/form")

if __name__=="__main__":
    # db.create_all()
    app.run(debug=True)