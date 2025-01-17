# app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from model import db, User, Goal
from config import Config
import bcrypt
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# 회원가입 페이지
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # 사용자 DB에 추가
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('회원가입 성공! 로그인하세요.')
        return redirect(url_for('login'))
    return render_template('signup.html')

# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            session['user_id'] = user.id
            flash('로그인 성공!')
            return redirect(url_for('home'))
        else:
            flash('아이디 또는 비밀번호가 잘못되었습니다.')
            return redirect(url_for('login'))
    return render_template('login.html')

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('로그아웃 성공!')
    return redirect(url_for('login'))

# 메인 화면 (목표 목록 표시)
@app.route('/home')
def home():
    if 'user_id' not in session:
        flash('로그인 후 이용해주세요.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_goals = Goal.query.filter_by(user_id=user_id).all()
    return render_template('home.html', goals=user_goals)

# 목표 추가 페이지
@app.route('/add_goal', methods=['GET', 'POST'])
def add_goal():
    if 'user_id' not in session:
        flash('로그인 후 이용해주세요.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        goal_name = request.form['goal_name']
        target_amount = float(request.form['target_amount'])
        deadline = request.form['deadline']
        save_frequency = request.form['save_frequency']
        user_id = session['user_id']

        new_goal = Goal(name=goal_name, target_amount=target_amount, deadline=deadline, save_frequency=save_frequency, user_id=user_id)
        db.session.add(new_goal)
        db.session.commit()

        flash('목표가 추가되었습니다!')
        return redirect(url_for('home'))

    return render_template('add_goal.html')

# 목표 진행 상황 페이지
@app.route('/goal/<int:goal_id>', methods=['GET', 'POST'])
def goal(goal_id):
    if 'user_id' not in session:
        flash('로그인 후 이용해주세요.')
        return redirect(url_for('login'))

    goal = Goal.query.get_or_404(goal_id)

    if request.method == 'POST':
        saved_amount = float(request.form['saved_amount'])
        goal.saved_amount += saved_amount  # 저축액 추가
        db.session.commit()

        flash(f'{saved_amount}원이 목표에 추가되었습니다!')
        return redirect(url_for('goal', goal_id=goal.id))

    # 진행률 계산
    progress = goal.progress()
    return render_template('goal_detail.html', goal=goal, progress=progress)

if __name__ == '__main__':
    app.run(debug=True)
