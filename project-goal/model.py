# model.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# 사용자 모델 (회원가입 및 로그인 정보 저장)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    goals = db.relationship('Goal', backref='user', lazy=True)

# 목표 모델 (목표 정보 및 저축 내역 저장)
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    saved_amount = db.Column(db.Float, default=0)  # 저축액 초기값 0
    deadline = db.Column(db.String(150), nullable=False)
    save_frequency = db.Column(db.String(50), nullable=False)  # ex: 'weekly', 'monthly'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def progress(self):
        """진행률을 계산하는 메서드"""
        return (self.saved_amount / self.target_amount) * 100 if self.target_amount else 0
