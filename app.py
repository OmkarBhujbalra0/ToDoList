# Below Code imports packages/modules that are important for handling requests,redirecting to the page,rendering the HTML file
from flask import Flask,render_template,request,redirect,flash

# Used Flask class to initialize the app
app = Flask(__name__)

# This key can be written manually or can be generated using hashing 
app.secret_key = 'your_secret_key'

# A list to add tasks
tasklist = []

# App Route
@app.route('/',methods=['GET','POST'])
def homepage():
    # If anything is added in the form then retrieve input and append it to the above defined list
    if request.method == 'POST':
        # Even If user enters only spaces in input field,strip() will remove the space and field will remain empty 
        task = request.form.get("task").strip()
        if not task:
            flash("Please Enter Something",'error')
            return redirect('/')
        if task in tasklist:
            flash("Task is already present in this list",'danger')
            return redirect('/')
        tasklist.append(task)
        # After each task is added ,page is redirected
        return redirect('/')
    return render_template('index.html',tasks=tasklist)

@app.route('/delete/<task>')
def delete(task):
    if task in tasklist:
        tasklist.remove(task)
    return redirect('/')

# Run the App
if __name__ == '__main__':
    app.run(debug=True)