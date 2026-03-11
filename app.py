from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import uuid
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = "supersecretkey"
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    user_id = db.Column(db.String(200),nullable = False)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

    



@app.route("/",methods = ['POST','GET'])
def hello_world():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    if request.method == "POST":
        todo = Todo(title=request.form['title'], desc=request.form['desc'],user_id = session['user_id'])
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    
    return render_template('index.html', allTodo = Todo.query.filter_by(user_id = session['user_id']).all()) 

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route("/edit/<int:sno>", methods = ['POST','GET'])
def edit(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    allTodo = Todo.query.filter_by(user_id = session['user_id']).all()
    if request.method == "POST":
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    
    return render_template("update.html",todo = todo, allTodo = allTodo)



if __name__ == "__main__":
    app.run(debug=True)