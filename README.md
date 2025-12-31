# To-Do List Application (Flask + SQLite)

Lightweight To-Do web application built with Python and Flask. It demonstrates simple CRUD APIs backed by SQLite (no ORM), server-rendered templates, basic logging/error handling, and automated tests using pytest.

## Key features
- RESTful JSON API for tasks (create, read, update, delete)
- Server-rendered UI using Jinja2 templates (`templates/tasks.html`, `templates/add_task.html`)
- Simple raw-SQL data layer in `db.py` with a reusable `init_db` function
- Tests that exercise the API using `pytest`

## Tech stack
- Python 3.10+
- Flask
- SQLite (file database)
- pytest (tests)

## Repository layout

```
To-Do-App/
├── app.py                # Flask application (routes, APIs, templates)
├── db.py                 # SQLite helper functions and CRUD operations
├── schema.sql            # Database schema
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── tasks.html        # Task listing page
│   └── add_task.html     # Add new task page
├── tests/                # Pytest test cases
│   └── test_task.py      # CRUD API tests
└── README.md             # This file
```

## Quick start

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows PowerShell
.\\.venv\\Scripts\\Activate.ps1
# or Command Prompt
.\\.venv\\Scripts\\activate.bat
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database and run the app:

```bash
python app.py
```

Running `app.py` directly will call `init_db()` and start the Flask development server.

Open http://127.0.0.1:5000 to view the app UI.

## Configuration

The app uses a simple file-based SQLite database. By default the database filename is `tasks.db`. You can override the database file used at runtime by setting `app.config['DB_NAME']` before starting the app (the test suite uses a temporary file).

## API Reference

All API endpoints are under `/api/tasks` and use JSON request/response bodies.

- Create task

	- URL: `POST /api/tasks`
	- Body (JSON):

		```json
		{
			"title": "Buy groceries",
			"description": "Milk, eggs",
			"due_date": "2025-12-31",
			"status": "pending"
		}
		```

	- Success: `201 Created` with `{"message": "Task created"}`

- List tasks

	- URL: `GET /api/tasks`
	- Success: `200 OK` with JSON array of tasks

- Get single task

	- URL: `GET /api/tasks/<id>`
	- Success: `200 OK` with task object, or `404` if not found

- Update task

	- URL: `PUT /api/tasks/<id>`
	- Body: partial or full task object (fields default to existing values)
	- Success: `200 OK` with `{"message": "Task updated"}`

- Delete task

	- URL: `DELETE /api/tasks/<id>`
	- Success: `200 OK` with `{"message": "Task deleted"}`

Example curl to create a task:

```bash
curl -s -X POST http://127.0.0.1:5000/api/tasks \\
	-H "Content-Type: application/json" \\
	-d '{"title":"Test","description":"desc","due_date":"2025-12-31","status":"pending"}'
```

## Templates / Web UI

- `/tasks` — server-rendered listing page using `templates/tasks.html` (shows count, status badges, and actions).
- `/add-task` — simple form to add tasks (`templates/add_task.html`).

Note: The UI includes disabled action buttons (Complete/Delete) because the example uses API endpoints; you can wire the UI to call the API (via forms or JavaScript) if you want active buttons.

## Database schema

See `schema.sql` for the table definition (simple `tasks` table):

```
CREATE TABLE IF NOT EXISTS tasks (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		description TEXT,
		due_date TEXT,
		status TEXT NOT NULL CHECK(status IN ('pending', 'completed'))
);
```

The `db.py` module exposes helper functions:

- `get_connection(db_name)` — returns a `sqlite3.Connection` with `row_factory` set.
- `init_db(db_name)` — executes `schema.sql` to create the table.
- `create_task(...)`, `get_all_tasks(db_name)`, `get_task_by_id(id, db_name)`, `update_task(...)`, `delete_task(id, db_name)`

## Tests

The test suite uses `pytest` and creates a temporary SQLite file for isolation. To run tests:

```bash
pytest -q
```

The tests live in the `tests/` folder and exercise the JSON API endpoints (`tests/test_task.py`).

## Logging & error handling

The application uses the standard `logging` module (`app.py`) to emit informational and error logs. API routes return `500` responses with a JSON error message on unexpected exceptions, and appropriate `4xx` responses for client errors.

## Development notes

- To change the DB file used by the app, set `app.config['DB_NAME']` before calling `init_db()` or running the server.
- Tests already configure `app.config['TESTING'] = True` and use a temporary DB file.

## Files to inspect

- `app.py` — Flask routes and template integration
- `db.py` — database helpers and CRUD functions
- `schema.sql` — DB schema
- `templates/tasks.html`, `templates/add_task.html` — UI
- `tests/test_task.py` — example API tests
