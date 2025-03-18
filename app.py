# Below Code imports packages/modules that are important for handling requests,redirecting to the page,rendering the HTML file
from flask import Flask,render_template,request,redirect,flash
from urllib.parse import unquote
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Used Flask class to initialize the app
app = Flask(__name__)

# This will configure Sqlite as db and creates tasks.db named database if it does not exist
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///tasks.db"

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    task = db.Column(db.String(200),nullable=False)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    priority = db.Column(db.String,nullable=False,default="Medium")
    completion = db.Column(db.String,nullable=False,default="Incomplete")

# Creates a DB if not created
with app.app_context():
    db.create_all()

# This key can be written manually or can be generated using hashing 
app.secret_key = 'your_secret_key'

# App Route
@app.route('/',methods=['GET','POST'])
def homepage():
    # If anything is added in the form then retrieve input and append it to the above defined list
    if request.method == 'POST':
        # Even If user enters only spaces in input field,strip() will remove the space and field will remain empty 
        task = request.form.get("task").strip()
        priority = request.form.get("priority")
        completion = request.form.get("completion")
        date = datetime.now()
        if not task:
            flash("Please Enter Something",'error')
            return redirect('/')
        task = Task(task=task,date=date,priority=priority,completion=completion)
        db.session.add(task)
        db.session.commit()
        print(task)
        # After each task is added ,page is redirected
        return redirect('/')
    Tasks = Task.query.all()
    return render_template('index.html',tasks=Tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    # Check if task is present in db,if not it returns 404 Error
    task = Task.query.get_or_404(id)
    Tasks = Task.query.all()
    # if task is present,take new input to replace old input(task)
    if request.method == 'POST':
        new_task = request.form.get("new_task")
        new_priority = request.form.get("new_priority")
        new_completion = request.form.get("new_completion")
        # Replaces old task with new task
        if not new_task.strip():
            flash("Please Enter Something",'error')
            return redirect(f'/edit/{id}')
        task.task = new_task
        task.priority = new_priority
        task.completion = new_completion
        db.session.commit()
        flash("Task successfully Edited","success")
            # If there is any error then page will redirect back to same page
        return redirect('/')
    return render_template('edit.html',task=task,tasks=Tasks)
    

# Run the App
if __name__ == '__main__':
    app.run(debug=True)