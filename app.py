from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, FloatField
from passlib.hash import sha256_crypt
from functools import wraps
from time import strftime, localtime, time
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True

#init db
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:admin123@localhost/webapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User_admin(db.Model):
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


class User_data(db.Model):
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

    def __init__(self, school_num, temperature, date):
        self.school_num = school_num
        self.temperature = temperature
        self.date = date


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

        user = User_admin(school_num, password, 0, name, phone)
        #用User_admin查询，不能用user，会出现永1的情况
        if User_admin.query.filter(
                User_admin.school_num == school_num).count() > 0:
            flash("该账号已注册", "warning")
            return redirect(url_for('login'))
        else:
            db.session.add(user)
            db.session.commit()

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

        if User_admin.query.filter(
                User_admin.school_num == school_num).count() > 0:
            result = User_admin.query.filter(
                User_admin.school_num == school_num).first()
            password = result.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['school_num'] = school_num
                session['rank'] = result.rank
                session['username'] = result.name
                flash('你已登录', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = '密码错误'
                return render_template('login.html', error=error)
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
    flash('您已退出登录', 'success')
    return redirect(url_for('login'))


# Dashboard


@app.route('/dashboard')
@is_logged_in
def dashboard():
    if session['rank']:
        users = User_data.query.all()
        count = User_data.query.count()
    else:
        users = User_data.query.filter(
            User_data.school_num == session['school_num']).all()
        count = User_data.query.filter(
            User_data.school_num == session['school_num']).count()

    if count > 0:
        return render_template('dashboard.html', users=users)
    else:
        msg = '没有记录'
        return render_template('dashboard.html', msg=msg)

    return render_template('dashboard.html')


@app.route('/admin_user', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def admin_user():
    users = User_admin.query.all()
    return render_template("admin_user.html", users=users)


@app.route('/admin_set/<string:school_num>', methods=['GET', 'POST'])
@is_logged_in
@is_admin
def admin_set(school_num):
    user = User_admin.query.filter(User_admin.school_num == school_num).first()
    if user.school_num == session['school_num']:
        flash('不能修改自身权限', 'warning')
        return redirect(url_for('admin_user'))
    user.rank = bool(1 - user.rank)
    db.session.commit()
    flash('权限已修改', 'success')
    return redirect(url_for('admin_user'))


class PunchForm(Form):
    temperature = FloatField('温度', [
        validators.NumberRange(
            min=35.0, max=45.0, message="体温必须在%(min)d，%(max)d之间")
    ])


@app.route('/punch_in', methods=['GET', 'POST'])
@is_logged_in
def punch_in():
    form = PunchForm(request.form)
    if request.method == 'POST' and form.validate():
        temperature = form.temperature.data

        date = strftime("%Y-%m-%d", localtime(time()))

        data = User_data(session['school_num'], temperature, date)
        #组合查询用filter_by
        if User_data.query.filter_by(school_num=session['school_num'],
                                     date=date).count():
            flash('今日已打卡', 'warning')
            return redirect(url_for('dashboard'))
        else:
            db.session.add(data)
            db.session.commit()
            return redirect(url_for('dashboard'))
        flash('打卡成功 ', 'success')

        return redirect(url_for('dashboard'))

    return render_template('punch_in.html', form=form)


@app.route('/edit_info/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_info(id):

    if id == session['school_num'] or session['rank']:
        pass
    else:
        flash('权限不够', 'warning')
        return redirect(url_for('dashboard'))

    user = User_admin.query.filter(User_admin.school_num == id).first()

    form = RegisterForm(request.form)

    form.name.data = user.name
    form.phone.data = user.phone
    form.school_num.data = user.school_num

    if request.method == 'POST' and form.validate():
        user.name = request.form['name']
        user.phone = request.form['phone']
        user.password = sha256_crypt.encrypt(str(request.form['password']))
        db.session.commit()
        flash('信息已更改', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_info.html', form=form)


@app.route('/delete_data/<string:school_num>/<string:date>', methods=['POST'])
@is_logged_in
@is_admin
def delete_data(school_num, date):

    data = User_data.query.filter_by(school_num=school_num, date=date).first()
    db.session.delete(data)
    db.session.commit()
    flash('已删除', 'success')

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(host="0.0.0.0")
