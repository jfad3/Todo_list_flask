from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))
    due_date = db.Column(db.String(10))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

@app.route('/task', methods=['POST'])
def add_task():
    data = request.get_json()
    new_task = Task(title=data['title'], description=data['description'], due_date=data['due_date'])

    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added.'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 400

@app.route('/task/<int:id>', methods=['GET'])
def get_task(id):
   task=Task.query.get(id)
   return jsonify({'title': task.title, 'description': task.description, 'due_date': task.due_date}), 200

@app.route('/task/<int:id>', methods=['PUT'])
def update_task(id):
   data=request.get_json()

   task=Task.query.get(id)
   task.title=data['title']
   task.description=data['description']
   task.due_date=data['due_date']

   try:
       db.session.commit()
       return jsonify({'message':'Task updated.'}),200
   except Exception as e:
       return jsonify({'message':str(e)}),400

@app.route('/task/<int:id>', methods=['DELETE'])
def delete_task(id):
   Task.query.filter_by(id=id).delete()

   try:
       db.session.commit()
       return jsonify({'message':'Task deleted.'}),200
   except Exception as e:
       return jsonify({'message':str(e)}),400

if __name__ == '__main__':
     app.run(debug=True)
