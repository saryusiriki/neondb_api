import psycopg2
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

NEON_CONN_STR = os.environ["NEON_CONN_STR"]

def connect_to_neon():
    return psycopg2.connect(NEON_CONN_STR)

@app.route("/")
def home():
    return "Hello, Neon API is running"

@app.route("/query", methods=["POST"])
def run_query():
    data = request.get_json()
    query = data.get("query")
    if not query:
        return jsonify({"status": "error", "message": "No query provided"}), 400

    conn = connect_to_neon()
    cursor = conn.cursor()

    try:
        cursor.execute(query)
        if cursor.description is None:
            return jsonify({"status": "success", "data": []})

        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        output = [dict(zip(columns, row)) for row in results]

        return jsonify({"status": "success", "data": output})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
