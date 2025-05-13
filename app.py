from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kanban.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models: Column, Task (as above)

@app.route('/move-task', methods=['POST'])
def move_task():
    data = request.get_json()
    task_id = data.get('task_id')
    to_column_id = data.get('to_column_id')
    new_position = data.get('new_position')  # Optional, else place at end

    if not task_id or not to_column_id:
        return jsonify({'error': 'task_id and to_column_id are required'}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    if task.column_id == to_column_id:
        return jsonify({'error': 'Task is already in the target column'}), 400

    to_column = Column.query.get(to_column_id)
    if not to_column:
        return jsonify({'error': 'Target column not found'}), 404

    # Remove task from current column by reordering the old column
    old_column_tasks = Task.query.filter_by(column_id=task.column_id).order_by(Task.position).all()
    for i, t in enumerate([t for t in old_column_tasks if t.id != task.id]):
        t.position = i

    # Fetch target column tasks
    target_tasks = Task.query.filter_by(column_id=to_column_id).order_by(Task.position).all()

    # Determine the insertion position
    if new_position is None or new_position > len(target_tasks):
        new_position = len(target_tasks)  # Place at end

    # Shift positions of other tasks in target column
    for i, t in enumerate(target_tasks):
        if i >= new_position:
            t.position = i + 1

    # Move the task
    task.column_id = to_column_id
    task.position = new_position
    db.session.commit()

    return jsonify({
        'message': 'Task moved successfully and position adjusted',
        'task': {
            'id': task.id,
            'title': task.title,
            'column_id': task.column_id,
            'position': task.position
        }
    }), 200


@app.route('/reorder-task', methods=['POST'])
def reorder_task():
    data = request.get_json()
    task_id = data.get('task_id')
    new_position = data.get('new_position')

    if task_id is None or new_position is None:
        return jsonify({'error': 'task_id and new_position are required'}), 400

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    column_id = task.column_id
    current_position = task.position

    if current_position == new_position:
        return jsonify({'message': 'No change needed'}), 200

    # Get all tasks in the same column, ordered by position
    tasks = Task.query.filter_by(column_id=column_id).order_by(Task.position).all()

    # Ensure new_position is within bounds
    if new_position < 0 or new_position >= len(tasks):
        return jsonify({'error': 'Invalid new position'}), 400

    # Remove the task from the list and insert at new position
    tasks.remove(task)
    tasks.insert(new_position, task)

    # Reassign positions
    for idx, t in enumerate(tasks):
        t.position = idx

    db.session.commit()

    return jsonify({
        'message': 'Task reordered successfully',
        'task': {
            'id': task.id,
            'column_id': task.column_id,
            'new_position': task.position
        }
    }), 200
    
    
    
@app.route('/boards/<int:board_id>/view', methods=['GET'])
def view_board(board_id):
    board = Board.query.get(board_id)
    if not board:
        return jsonify({'error': 'Board not found'}), 404

    # Prepare nested structure
    result = {
        'board_id': board.id,
        'board_name': board.name,
        'columns': []
    }

    # Sort columns by order_on_board
    columns = Column.query.filter_by(board_id=board.id).order_by(Column.order_on_board).all()

    for column in columns:
        tasks = Task.query.filter_by(column_id=column.id).order_by(Task.position).all()
        task_list = [{
            'task_id': task.id,
            'title': task.title,
            'order_in_column': task.position
        } for task in tasks]

        result['columns'].append({
            'column_id': column.id,
            'column_name': column.name,
            'order_on_board': column.order_on_board,
            'tasks': task_list
        })

    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True)
