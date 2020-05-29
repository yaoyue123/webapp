from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FloatField
from passlib.hash import sha256_crypt
from functools import wraps
from time import strftime, localtime, time
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin123'
app.config['MYSQL_DB'] = 'webapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class user_admin(db.Model):
    __tablename__ = 'user_admin'
    school_num = db.Column(db.String(13), primary_key=True)
    password = db.Column(db.Text, nullable=False)
    rank = db.Column(db.Boolean, nullable=False)
    name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(11), nullable=False)

    def __init__(self, school_num, password, rank, name, phone):
        self.school_num = school_num
        self.password = password
        self.rank = rank
        self.name = name
        self.phone = phone

    def __repr__(self):
        return '<school_num %r>' % self.school_num


class user_data(db.Model):
    __tablename__ = 'user_data'
    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   nullable=False)
    school_num = db.Column(db.String(13),
                           db.ForeignKey('user_admin.school_num'),
                           nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, school_num, password, rank, name, phone):
        self.id = id
        self.school_num = school_num
        self.temperature = temperature
        self.date = date

    def __repr__(self):
        return '<school_num %r>' % self.school_num


db.create_all()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/articles')
def articles():

    # create cursor
    cur = mysql.connection.cursor()

    # get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # close connection
    cur.close()


@app.route('/article/<string:id>/')
def article(id):
    # create cursor
    cur = mysql.connection.cursor()

    # get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


class RegisterForm(Form):
    name = StringField('姓名', [validators.Length(min=1, max=8)])
    school_num = StringField('学号', [validators.Length(min=13, max=13)])
    phone = StringField('电话',
                        [validators.Length(min=11, max=11, message="号码格式错误")])
    password = PasswordField('密码', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='两次密码不一致')
    ])
    confirm = PasswordField('确认密码')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        school_num = form.school_num.data
        phone = form.phone.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create crusor
        cur = mysql.connection.cursor()

        # 返回成功记录数
        if cur.execute(
                "SELECT school_num FROM user_admin WHERE school_num = %s",
            [school_num]) == 0:
            cur.execute(
                "INSERT INTO user_admin(school_num,password,rank,name,phone) VALUES(%s,%s,0,%s,%s)",
                (school_num, password, name, phone))
        else:
            flash("该账号已注册", "warning")
            return redirect(url_for('login'))

        # commit to DB
        mysql.connection.commit()
        # close connection
        cur.close()

        flash("您的账号已经注册好了，请登录", 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# user login


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        school_num = request.form['school_num']
        password_candidate = request.form['password']

        # Create cursor

        cur = mysql.connection.cursor()

        # Get user by username

        result = cur.execute("SELECT * FROM user_admin WHERE school_num = %s",
                             [school_num])

        if result > 0:
            # Get Stored hash
            user = cur.fetchone()
            password = user['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['school_num'] = school_num
                session['rank'] = user['rank']
                session['username'] = user['name']
                flash('你已登录', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = '密码错误'
                return render_template('login.html', error=error)
                # close connection
            cur.close()

        else:
            error = '当前学号不存在，请注册'
            return render_template('login.html', error=error)

    return render_template('login.html')


# check if user logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('请登录', 'danger')
            return redirect(url_for('login'))

    return wrap


def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['rank'] == 1:
            return f(*args, **kwargs)
        else:
            flash('权限不够', 'danger')
            return redirect(url_for('dashboard'))

    return wrap


# logout


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('you are now logged out ', 'success')
    return redirect(url_for('login'))


# Dashboard


@app.route('/dashboard')
@is_logged_in
def dashboard():

    # create cursor
    cur = mysql.connection.cursor()

    if session['rank']:
        result = cur.execute("SELECT * FROM user_data WHERE 1")
        users = cur.fetchall()
    else:
        result = cur.execute("SELECT * FROM user_data WHERE school_num = %s",
                             [session['school_num']])
        users = cur.fetchall()

    # get articles
    #result = cur.execute("SELECT * FROM user_data WHERE 1")
    #users = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', users=users)
    else:
        msg = 'No data Found'
        return render_template('dashboard.html', msg=msg)
    # close connection
    cur.close()
    return render_template('dashboard.html')


@app.route('/admin_user', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def admin_user():
    cur = mysql.connection.cursor()

    return render_template("admin_user.html")


class PunchForm(Form):
    temperature = FloatField('温度', [
        validators.NumberRange(
            min=35.0, max=45.0, message="体温必须在%(min)d，%(max)d之间")
    ])


# Add Article


@app.route('/punch_in', methods=['GET', 'POST'])
@is_logged_in
def punch_in():
    form = PunchForm(request.form)
    if request.method == 'POST' and form.validate():
        temperature = form.temperature.data
        # Create a cursor
        date = strftime("%Y-%m-%d", localtime(time()))
        cur = mysql.connection.cursor()

        # execute

        if cur.execute(
                "SELECT * FROM user_data WHERE school_num = %s AND date = %s",
            (session['school_num'], date)):
            flash('今日已打卡', 'warning')
            return redirect(url_for('dashboard'))
        else:
            cur.execute(
                "INSERT INTO user_data(school_num,temperature,date) VALUES(%s, %s, %s)",
                (session['school_num'], temperature, date))

        # commit to db

        mysql.connection.commit()

        # close connection
        cur.close()

        flash('打卡成功 ', 'success')

        return redirect(url_for('dashboard'))

    return render_template('punch_in.html', form=form)


# Edit Article
@app.route('/edit_info/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_info(id):
    # Create cursor
    cur = mysql.connection.cursor()
    # get article by id
    if id == session['school_num'] or session['rank']:
        pass
    else:
        flash('权限不够', 'warning')
        return redirect(url_for('dashboard'))
    result = cur.execute("SELECT * FROM user_admin WHERE school_num = %s",
                         [id])

    user = cur.fetchone()

    # get form
    form = RegisterForm(request.form)

    # populate article form fields
    form.name.data = user['name']
    form.phone.data = user['phone']
    form.school_num.data = user['school_num']

    if request.method == 'POST' and form.validate():
        name = request.form['name']
        phone = request.form['phone']
        password = sha256_crypt.encrypt(str(request.form['password']))
        # Create a cursor
        cur = mysql.connection.cursor()
        # execute

        cur.execute(
            "UPDATE user_admin SET name=%s, phone=%s,password = %s WHERE school_num = %s",
            (name, phone, password, id))

        # commit to db

        mysql.connection.commit()

        # close connection
        cur.close()

        flash('信息已更改', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_info.html', form=form)


# Delete article


@app.route('/delete_data/<string:school_num>/<string:date>', methods=['POST'])
@is_logged_in
@is_admin
def delete_data(school_num, date):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM user_data WHERE school_num = %s AND date = %s",
                (school_num, date))

    # Commit to DB

    mysql.connection.commit()
    # close connection

    cur.close()

    flash('已删除', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host="0.0.0.0")
