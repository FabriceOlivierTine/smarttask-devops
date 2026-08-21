from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import time

app = Flask(__name__)
CORS(app)

DB_HOST = os.environ.get("DB_HOST", "database")
DB_NAME = os.environ.get("DB_NAME", "smarttask")
DB_USER = os.environ.get("DB_USER", "smarttask_user")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "smarttask_pass")
DB_PORT = os.environ.get("DB_PORT", "5432")


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )


def init_db():
    """Attend que la base soit prête, puis crée la table si besoin."""
    for attempt in range(10):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    status VARCHAR(50) DEFAULT 'todo',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            conn.commit()
            cur.close()
            conn.close()
            print("Base de données initialisée avec succès.")
            return
        except Exception as e:
            print(f"Tentative {attempt + 1}/10 - base non prête ({e}), retry dans 3s...")
            time.sleep(3)
    print("Impossible de se connecter à la base de données après plusieurs tentatives.")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM tasks ORDER BY created_at DESC;")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(tasks), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "todo")

    if not title:
        return jsonify({"error": "Le titre est requis"}), 400

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s) RETURNING *;",
        (title, description, status),
    )
    new_task = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    status = data.get("status")

    conn = get_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute(
        "UPDATE tasks SET status = %s WHERE id = %s RETURNING *;",
        (status, task_id),
    )
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if not updated:
        return jsonify({"error": "Tâche introuvable"}), 404
    return jsonify(updated), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s;", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Tâche supprimée"}), 200


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
