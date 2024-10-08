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
    # 현재 페이지 번호를 URL에서 가져오고, 기본값은 1로 설정
    page = request.args.get('page', 1, type=int)
    per_page = 7  # 한 페이지당 표시할 항목 수

    # 페이지네이션을 이용해 할 일 목록 가져오기
    pagination = Todo.query.paginate(page=page, per_page=per_page, error_out=False)
    todos = pagination.items  # 현재 페이지에 해당하는 할 일 목록

    # 페이지네이션 정보를 넘겨줌
    return render_template('index.html', todos=todos, pagination=pagination)

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
    
@app.route('/edit/<int:id>', methods=['POST','GET'])
def edit_by_id(id):
    todo = Todo.query.get_or_404(id)
    if request.method == 'GET':
        return render_template('edit.html', todo=todo)

    elif request.method == 'POST':
        data = request.form
        todo.title = data['title']
        todo.description = data['description']
        # 데이터베이스에 수정 사항을 저장
        db.session.commit()
        return redirect(url_for('index'))

# 오류가 나는 상황 *** -> Search 기능 제대로 구현이 안되고 있음 
@app.route('/search', methods=['GET'])
def search():
    data = request.args
    print("search called")
    word = data['word']
    if not word:
        return redirect(url_for('index'))
    todos = Todo.query.filter(Todo.title.like(f'%{word}%')).all()
    return render_template('index.html', todos=todos)


@app.route('/update_completed/<int:id>', methods=['POST'])
def update_completed(id):
    data = request.get_json()
    completed = data.get('completed')

    todo = Todo.query.get_or_404(id)
    todo.completed = completed

    try:
        db.session.commit()
        return jsonify({'success': True})
    except:
        db.session.rollback()
        return jsonify({'success': False}), 500

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
