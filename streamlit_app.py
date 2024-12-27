from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
import secrets

app = Flask(__name__)

# Database setup
def setup_database():
    conn = sqlite3.connect("license_keys.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS license_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            license_key TEXT UNIQUE NOT NULL,
            user_name TEXT,
            email TEXT,
            expiration_date TEXT,
            plan_type TEXT,
            platforms TEXT,
            is_active INTEGER DEFAULT 1
        )
    """)
    conn.commit()
    conn.close()

setup_database()

# Generate license key
@app.route('/generate_license', methods=['POST'])
def generate_license():
    data = request.json
    user_name = data.get("user_name")
    email = data.get("email")
    expiration_date = data.get("expiration_date")
    plan_type = data.get("plan_type")
    platforms = ",".join(data.get("platforms", []))

    if not (user_name and email and expiration_date and plan_type and platforms):
        return jsonify({"status": "error", "message": "Missing required fields."}), 400

    license_key = f"RBT-{secrets.token_hex(8).upper()}"

    conn = sqlite3.connect("license_keys.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO license_keys (license_key, user_name, email, expiration_date, plan_type, platforms, is_active)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    """, (license_key, user_name, email, expiration_date, plan_type, platforms))
    conn.commit()
    conn.close()

    return jsonify({"status": "success", "license_key": license_key})

# Validate license key
@app.route('/validate_license', methods=['POST'])
def validate_license():
    data = request.json
    license_key = data.get("license_key")

    conn = sqlite3.connect("license_keys.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM license_keys WHERE license_key = ?", (license_key,))
    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({"status": "error", "message": "License key not found."}), 404

    _, _, user_name, email, expiration_date, plan_type, platforms, is_active = result

    if not is_active:
        return jsonify({"status": "error", "message": "License key is inactive."}), 403

    if datetime.strptime(expiration_date, "%Y-%m-%d") < datetime.now():
        return jsonify({"status": "error", "message": "License key has expired."}), 403

    return jsonify({
        "status": "success",
        "license_info": {
            "user_name": user_name,
            "email": email,
            "expiration_date": expiration_date,
            "plan_type": plan_type,
            "platforms": platforms.split(",")
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
