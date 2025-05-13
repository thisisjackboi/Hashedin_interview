from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Column(db.Model):
    __tablename__ = 'columns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Task', backref='column', lazy=True)
    
class Board(db.Model):
    __tablename__ = 'boards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    columns = db.relationship('Column', backref='board', lazy=True, order_by='Column.order_on_board')

class Column(db.Model):
    __tablename__ = 'columns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    order_on_board = db.Column(db.Integer, nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('boards.id'), nullable=False)
    tasks = db.relationship('Task', backref='column', lazy=True, order_by='Task.position')

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    position = db.Column(db.Integer, nullable=False)  # order_in_column
    column_id = db.Column(db.Integer, db.ForeignKey('columns.id'), nullable=False)
