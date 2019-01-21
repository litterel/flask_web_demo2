# encoding: utf-8
from app import app, db
from flask import render_template, request, redirect, url_for, session, flash
from .models import User, Sample, Exp, Preuser
from .forms import RegisterForm, LoginForm
from .decorators import login_required

from sqlalchemy import or_


@app.route('/')
@app.route('/index')
def index():
    context = {
        'samples': Sample.query.order_by('-create_time').all()
    }
    return render_template('index.html', **context)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter(User.username == form.username.data, User.password == form.password.data).first()

        if not user:
            flash(u'用户名或密码有误')
            return redirect(url_for('login', form=form))

        session['user_id'] = user.id
        session.permanent = True
        # flash('欢迎' + form.username.data)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/regist/', methods=['GET', 'POST'])
def regist():
    form = RegisterForm()
    if form.validate_on_submit():

        uid = User.query.filter(User.username == form.username.data).first()
        if uid:
            flash(u'用户名已存在，请更换')
            return redirect(url_for('regist', form=form))

        user = Preuser(studentid=form.studentid.data, username=form.username.data, password=form.password.data,
                       description=form.description.data)
        db.session.add(user)
        db.session.commit()
        return u'申请已提交，等待管理员通过'
    return render_template('regist.html', form=form)


#########################################用户管理与preuser、user list
@app.route('/preuser/')
@login_required
def preuser():
    user_id = session['user_id']
    if user_id == 1:
        context1 = {
            'preusers': Preuser.query.order_by('studentid').all()
        }
        context2 = {
            'users': User.query.order_by('studentid').all()
        }
        return render_template('preuser.html', **context1, **context2)
    else:
        flash('你不是管理员，没有权限操作!')
        return redirect(url_for('index'))


@app.route('/add_user/<int:id>')
@login_required
def add_user(id):
    user_id = session['user_id']
    if user_id == 1:
        preuser = Preuser.query.get(id)
        user = User(studentid=preuser.studentid, username=preuser.username, password=preuser.password,
                    description=preuser.description)
        db.session.add(user)
        db.session.delete(preuser)
        db.session.commit()
        flash('操作成功')
    else:
        flash('你不是管理员，没有权限操作!')
    return redirect(url_for('preuser'))


@app.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    user_id = session['user_id']
    if user_id == 1:
        user = User.query.get(id)
        if user.id == user_id:
            flash('不能删除管理员')
        else:
            db.session.delete(user)
            db.session.commit()
            flash('操作成功')
    else:
        flash('你不是管理员，没有权限操作')
    return redirect(url_for('preuser'))


# 判断用户是否登录，只要我们从session中拿到数据就好了   注销函数
@app.route('/logout/')
def logout():
    # session.pop('user_id')
    # del session('user_id')
    session.clear()
    return redirect(url_for('login'))


@app.route('/sample/', methods=['GET', 'POST'])
@login_required
def sample():
    if request.method == 'GET':
        return render_template('sample.html')
    else:
        name = request.form.get('name')
        detail = request.form.get('detail')
        sample = Sample(name=name, detail=detail)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        sample.author = user
        db.session.add(sample)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/detail/<sample_id>/')
def detail(sample_id):
    sample_model = Sample.query.filter(Sample.id == sample_id).first()
    return render_template('detail.html', sample=sample_model)


@app.route('/add_exp/', methods=['POST'])
@login_required
def add_exp():
    result = request.form.get('exp_result')
    sample_id = request.form.get('sample_id')
    exp = Exp(result=result)
    user_id = session['user_id']
    user = User.query.filter(User.id == user_id).first()
    exp.author = user
    sample = Sample.query.filter(Sample.id == sample_id).first()
    exp.sample = sample
    db.session.add(exp)
    db.session.commit()
    return redirect(url_for('detail', sample_id=sample_id))


@app.route('/delete_exp/<int:id>')
@login_required
def delete_exp(id):
    # exp = Exp.query.filter(id == id).first_or_404()
    exp = Exp.query.get(id)
    enu = exp.sample_id
    user_id = session['user_id']
    if user_id == 1:
        db.session.delete(exp)
        db.session.commit()
        flash('删除成功')
    else:
        flash('你不是管理员，没有权限操作')
    return redirect(url_for('detail', sample_id=enu))


@app.route('/search/')
def search():
    q = request.args.get('q')
    # title, content
    # 或 查找方式（通过标题和内容来查找）
    # questions = Question.query.filter(or_(Question.title.contains(q),
    #                                     Question.content.constraints(q))).order_by('-create_time')
    # 与 查找（只能通过标题来查找）
    samples = Sample.query.filter(Sample.name.contains(q), Sample.detail.contains(q))
    return render_template('index.html', samples=samples)


# 钩子函数(注销)

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run(debug=True)
