from flask import Flask, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import render_template


app = Flask(__name__)

# 데이터베이스 설정
# username에는 생성한 사용자 계정명 입력
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask_user:password@localhost/flask_todo_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SQLAlchemy 객체 생성
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    def __repr__(self):
        return f'<Todo {self.title}>'


@app.route('/')
def index():
    tmp = Todo.query.all()
    todos = []
    for todo in tmp:
        todos.append({
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'completed': todo.completed,
            'created_at': todo.created_at
        })
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add():
    print("add called")
    data = request.form

    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400

    title = data['title']
    description = data['description']

    new_todo = Todo(
            title=title,
            description=description
            )

    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_by_id(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))
    


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
