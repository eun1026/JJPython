from flask import Flask, render_template, request, redirect, url_for
from model import db, Goal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///goals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    goals = Goal.query.all()
    return render_template('index.html', goals=goals)

@app.route('/add', methods=['GET', 'POST'])
def add_goal():
    if request.method == 'POST':
        goal_name = request.form['goal-name']
        goal_amount = request.form['goal-amount']
        goal_deadline = request.form['goal-deadline']
        saving_frequency = request.form['saving-frequency']

        new_goal = Goal(name=goal_name, amount=goal_amount, deadline=goal_deadline, frequency=saving_frequency)
        db.session.add(new_goal)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:goal_id>', methods=['GET', 'POST'])
def edit_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    if request.method == 'POST':
        goal.name = request.form['edit-goal-name']
        goal.amount = request.form['edit-goal-amount']
        goal.deadline = request.form['edit-goal-deadline']
        goal.frequency = request.form['edit-saving-frequency']
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', goal=goal)

@app.route('/view/<int:goal_id>')
def view_goal(goal_id):
    goal = Goal.query.get_or_404(goal_id)
    return render_template('view.html', goal=goal)

if __name__ == '__main__':
    app.run(debug=True)
