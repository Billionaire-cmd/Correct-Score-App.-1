import streamlit as st
from tinydb import TinyDB, Query
from datetime import datetime
import secrets

# Setup TinyDB
db = TinyDB("license_keys.json")
License = Query()

# Generate License Key Function
def generate_license_key(user_name, email, expiration_date, plan_type, platforms):
    license_key = f"RBT-{secrets.token_hex(8).upper()}"
    db.insert({
        "license_key": license_key,
        "user_name": user_name,
        "email": email,
        "expiration_date": expiration_date,
        "plan_type": plan_type,
        "platforms": platforms,
        "is_active": True
    })
    return license_key

# Validate License Key Function
def validate_license_key(license_key):
    result = db.search(License.license_key == license_key)
    if not result:
        return {"status": "error", "message": "License key not found."}
    
    license_info = result[0]
    if not license_info["is_active"]:
        return {"status": "error", "message": "License key is inactive."}
    
    if datetime.strptime(license_info["expiration_date"], "%Y-%m-%d") < datetime.now():
        return {"status": "error", "message": "License key has expired."}

    return {"status": "success", "license_info": license_info}

# Streamlit App
st.title("License Key Management System")

# Tabs for Generate and Validate
tab1, tab2 = st.tabs(["Generate License Key", "Validate License Key"])

# Generate License Key
with tab1:
    st.header("Generate a New License Key")
    user_name = st.text_input("User Name")
    email = st.text_input("Email")
    expiration_date = st.date_input("Expiration Date", min_value=datetime.now().date())
    plan_type = st.selectbox("Plan Type", ["Basic", "Premium", "Enterprise"])
    platforms = st.multiselect("Platforms", ["MT4", "MT5", "Other"])

    if st.button("Generate License Key"):
        if user_name and email and platforms:
            license_key = generate_license_key(
                user_name, email, expiration_date.strftime("%Y-%m-%d"), plan_type, platforms
            )
            st.success(f"License Key Generated: {license_key}")
        else:
            st.error("Please fill all the required fields.")

# Validate License Key
with tab2:
    st.header("Validate an Existing License Key")
    license_key_to_validate = st.text_input("Enter License Key to Validate")

    if st.button("Validate License Key"):
        if license_key_to_validate:
            validation_result = validate_license_key(license_key_to_validate)
            if validation_result["status"] == "success":
                st.success("License Key is valid!")
                st.json(validation_result["license_info"])
            else:
                st.error(validation_result["message"])
        else:
            st.error("Please enter a License Key.")
