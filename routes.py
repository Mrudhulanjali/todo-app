from flask import Blueprint, render_template, request, redirect, url_for, session
from . import mongo
from bson.objectid import ObjectId
from datetime import datetime

task_bp = Blueprint('task', __name__)

@task_bp.route('/')
def home():
    return redirect(url_for('auth.login'))

@task_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    tasks = mongo.db.tasks.find({'user': session['username']})
    return render_template('dashboard.html', tasks=tasks)

@task_bp.route('/add', methods=['GET', 'POST'])
def add_task():
    if 'username' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        task = {
            'user': session['username'],
            'title': request.form['title'],
            'category': request.form['category'],
            'due_date': datetime.strptime(request.form['due_date'], '%Y-%m-%d'),
            'done': False
        }
        mongo.db.tasks.insert_one(task)
        return redirect(url_for('task.dashboard'))

    return render_template('add_task.html')

@task_bp.route('/complete/<task_id>')
def complete_task(task_id):
    mongo.db.tasks.update_one({'_id': ObjectId(task_id)}, {'$set': {'done': True}})
    return redirect(url_for('task.dashboard'))

@task_bp.route('/delete/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('task.dashboard'))
