from flask import Flask, request, jsonify
from datetime import datetime
import secrets
from tinydb import TinyDB, Query
from tinydb.operations import delete

app = Flask(__name__)

# Initialize TinyDB
db = TinyDB('license_keys.json')
licenses = db.table('licenses')

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

    licenses.insert({
        "license_key": license_key,
        "user_name": user_name,
        "email": email,
        "expiration_date": expiration_date,
        "plan_type": plan_type,
        "platforms": platforms,
        "is_active": True
    })

    return jsonify({"status": "success", "license_key": license_key})

# Validate license key
@app.route('/validate_license', methods=['POST'])
def validate_license():
    data = request.json
    license_key = data.get("license_key")

    License = Query()
    result = licenses.get(License.license_key == license_key)

    if not result:
        return jsonify({"status": "error", "message": "License key not found."}), 404

    if not result["is_active"]:
        return jsonify({"status": "error", "message": "License key is inactive."}), 403

    if datetime.strptime(result["expiration_date"], "%Y-%m-%d") < datetime.now():
        return jsonify({"status": "error", "message": "License key has expired."}), 403

    return jsonify({
        "status": "success",
        "license_info": {
            "user_name": result["user_name"],
            "email": result["email"],
            "expiration_date": result["expiration_date"],
            "plan_type": result["plan_type"],
            "platforms": result["platforms"].split(",")
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
