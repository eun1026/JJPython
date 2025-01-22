from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Date, nullable=False)
    frequency = db.Column(db.String(20), nullable=False)
    savings = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<Goal {self.name}>'