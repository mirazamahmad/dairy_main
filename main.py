from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'my_top_secret_123'
db = SQLAlchemy(app)


#Задание №1. Создай таблицу БД
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String, nullable=False)
    user_email = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        super(Card, self).__init__(**kwargs)

    def __repr__(self):
        return f'<Card {self.id}>'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __repr__(self):
        return f"<User {self.id}>"


@app.route('/')
def index():
    #Задание №2. Отоброзить объекты из БД в index.html
    email = session.get('user_email')
    if not email:
        return redirect('/login')
    cards = Card.query.filter_by(user_email=email).all()

    return render_template('index.html', cards=cards)


@app.route('/card/<int:id>')
def card(id):
    #Задание №2. Отоброзить нужную карточку по id
    card = Card.query.get(id)

    return render_template('card.html', card=card)


@app.route('/create')
def create():
    return render_template('create_card.html')


@app.route('/form_create', methods=['GET', 'POST'])
def form_create():
    if request.method == 'POST':
        title = request.form['title']
        subtitle = request.form['subtitle']
        text = request.form['text']

        #Задание №2. Создайте сопосб записи данных в БД
        email = session['user_email']
        card = Card(title=title, subtitle=subtitle, text=text, user_email=email)
        db.session.add(card)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create_card.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #Задание №3. Создай код для записи пользователя в БД
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_login = request.form['email']
        form_password = request.form['password']

        #Задание №4. Создай код для проверки пользователя в БД
        users_db = User.query.all()

        for user in users_db:
            if form_login == user.email and form_password == user.password:
                session['user_email'] = user.email
                return redirect('/')

        error = 'Неправильно указан пользователь или пароль'
        return render_template('login.html', error=error)
    else:
        return render_template('login.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)