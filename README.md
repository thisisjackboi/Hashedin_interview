
# 🗂️ Kanban Board API - Flask

This is a simple Kanban board API built using **Flask** and **SQLAlchemy**. It supports tasks, columns, and boards with features like drag-and-drop reordering and cross-column task movement.

---

## 🚀 Features

- View board with columns and ordered tasks
- Move tasks across columns
- Reorder tasks within the same column
- JSON API endpoints
- SQLite database for local development

---

## 📦 Folder Structure

```

Kanban-Flask-App/
├── app.py
├── models.py
├── requirements.txt
├── README.md
└── migrations/

````

---

## 🛠️ Setup Instructions

```bash
# Clone the repo
git clone https://github.com/thisisjackboi/Hashedin_interview.git
cd Hashedin_interview

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
flask run
````

---

## 📌 Key Endpoints

### View Board

```http
GET /boards/<board_id>/view
```

### Move Task

```http
POST /move-task
Body:
{
  "task_id": 1,
  "to_column_id": 2,
  "new_position": 0
}
```

### Reorder Task

```http
POST /reorder-task
Body:
{
  "task_id": 1,
  "new_position": 2
}
```

---

## 📋 Tech Stack

* Python 3.x
* Flask
* SQLAlchemy
* SQLite (dev)

---

## 📄 License

MIT License

```

---
```
