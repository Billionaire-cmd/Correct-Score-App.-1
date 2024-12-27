import streamlit as st
import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from threading import Thread

# Flask Backend for License Key Validation
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///licenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# License Key Model
class LicenseKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(255), unique=True, nullable=False)
    user_name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    expiration_date = db.Column(db.Date, nullable=False)
    plan_type = db.Column(db.String(50))
    platforms = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

# Initialize the database
with app.app_context():
    db.create_all()

@app.route('/validate_key', methods=['POST'])
def validate_key():
    data = request.json
    license_key = data.get("license_key")

    if not license_key:
        return jsonify({"status": "error", "message": "License key is required."}), 400

    key = LicenseKey.query.filter_by(license_key=license_key).first()

    if not key:
        return jsonify({"status": "error", "message": "Invalid license key."}), 404

    if not key.is_active:
        return jsonify({"status": "error", "message": "License key is inactive."}), 403

    if key.expiration_date < datetime.now().date():
        return jsonify({"status": "error", "message": "License key has expired."}), 403

    return jsonify({
        "status": "success",
        "license_info": {
            "user_name": key.user_name,
            "email": key.email,
            "expiration_date": key.expiration_date,
            "plan_type": key.plan_type,
            "platforms": key.platforms
        }
    })

# Run Flask in a separate thread
def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

Thread(target=run_flask).start()

# Streamlit App Interface
st.title("📉📈License Key Validation and Bot Activation")

# Form for entering license key
with st.form("License Validation"):
    license_key = st.text_input("Enter your License Key")
    submit_button = st.form_submit_button("Validate License")

if submit_button:
    if license_key:
        # Call the Flask API
        api_url = "http://localhost:5000/validate_key"
        response = requests.post(api_url, json={"license_key": license_key})

        if response.status_code == 200:
            data = response.json()
            st.success("License Validated!")
            st.write("License Details:")
            st.json(data["license_info"])
            st.info("You can now start the bot!")
        else:
            error_message = response.json().get("message", "Unknown error")
            st.error(f"Validation Failed: {error_message}")
    else:
        st.warning("Please enter a license key.")

