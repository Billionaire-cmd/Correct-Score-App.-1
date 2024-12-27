import streamlit as st
import sqlite3
from datetime import datetime
import secrets

# Step 1: Database setup
def setup_database():
    """Create the database table for license keys if it doesn't exist."""
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

def add_license_to_db(license_key, user_name, email, expiration_date, plan_type, platforms):
    """Insert a new license key into the database."""
    conn = sqlite3.connect("license_keys.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO license_keys (license_key, user_name, email, expiration_date, plan_type, platforms, is_active)
        VALUES (?, ?, ?, ?, ?, ?, 1)
    """, (license_key, user_name, email, expiration_date, plan_type, platforms))
    conn.commit()
    conn.close()

def validate_license_key(license_key):
    """Validate the license key."""
    conn = sqlite3.connect("license_keys.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM license_keys WHERE license_key = ?", (license_key,))
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return "Invalid", "License key not found in the database."

    # Unpack result
    _, _, user_name, email, expiration_date, plan_type, platforms, is_active = result
    
    if not is_active:
        return "Inactive", "This license key is inactive."

    if datetime.strptime(expiration_date, "%Y-%m-%d") < datetime.now():
        return "Expired", "This license key has expired."

    return "Valid", {
        "user_name": user_name,
        "email": email,
        "expiration_date": expiration_date,
        "plan_type": plan_type,
        "platforms": platforms
    }

def generate_license_key():
    """Generate a new license key."""
    return f"RBT-{secrets.token_hex(8).upper()}"

# Step 2: Streamlit UI
st.title("License Key Management System")
setup_database()

# Tab navigation
tab1, tab2 = st.tabs(["Validate License", "Generate License"])

# Tab 1: Validate License Key
with tab1:
    st.header("Validate License Key")
    license_key = st.text_input("Enter your License Key:")
    if st.button("Validate"):
        if not license_key:
            st.error("Please enter a license key.")
        else:
            status, info = validate_license_key(license_key)
            if status == "Valid":
                st.success("License key is valid!")
                st.write("### License Information:")
                st.write(f"- **User Name:** {info['user_name']}")
                st.write(f"- **Email:** {info['email']}")
                st.write(f"- **Expiration Date:** {info['expiration_date']}")
                st.write(f"- **Plan Type:** {info['plan_type']}")
                st.write(f"- **Platforms:** {info['platforms']}")
            else:
                st.error(info)

# Tab 2: Generate License Key
with tab2:
    st.header("Generate a New License Key")
    user_name = st.text_input("User Name")
    email = st.text_input("Email")
    expiration_date = st.date_input("Expiration Date")
    plan_type = st.selectbox("Plan Type", ["Basic", "Premium", "Enterprise"])
    platforms = st.multiselect("Platforms", ["MT4", "MT5", "Web"])
    
    if st.button("Generate Key"):
        if not (user_name and email and expiration_date and plan_type and platforms):
            st.error("Please fill out all fields to generate a license key.")
        else:
            new_key = generate_license_key()
            add_license_to_db(
                new_key,
                user_name,
                email,
                expiration_date.strftime("%Y-%m-%d"),
                plan_type,
                ",".join(platforms)
            )
            st.success(f"License key generated successfully: {new_key}")
