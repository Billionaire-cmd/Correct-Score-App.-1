import streamlit as st
from datetime import datetime

# Example license key database
license_db = {
    "RBT-4E12ABCD1234EF56": {
        "user_name": "John Doe",
        "email": "john@example.com",
        "expiration_date": "2025-12-31",
        "plan_type": "Premium",
        "platforms": "MT4,MT5",
        "is_active": True
    },
    "RBT-1234567890ABCDEF": {
        "user_name": "Jane Smith",
        "email": "jane@example.com",
        "expiration_date": "2024-12-31",
        "plan_type": "Basic",
        "platforms": "MT5",
        "is_active": False
    }
}

# Streamlit app layout
st.title("License Key Validation System")

# Input field for the license key
license_key = st.text_input("Enter your License Key")

if st.button("Validate License Key"):
    if not license_key:
        st.error("License Key is required.")
    else:
        # Check if the license key exists in the database
        license_info = license_db.get(license_key)
        if license_info:
            # Check if the license key is active
            if not license_info["is_active"]:
                st.error("License key is inactive.")
            else:
                # Check if the license key has expired
                expiration_date = datetime.strptime(license_info["expiration_date"], "%Y-%m-%d")
                if expiration_date < datetime.now():
                    st.error("License key has expired.")
                else:
                    # Display license information
                    st.success("License key is valid!")
                    st.write("### License Information:")
                    st.write(f"- **User Name:** {license_info['user_name']}")
                    st.write(f"- **Email:** {license_info['email']}")
                    st.write(f"- **Expiration Date:** {license_info['expiration_date']}")
                    st.write(f"- **Plan Type:** {license_info['plan_type']}")
                    st.write(f"- **Platforms:** {license_info['platforms']}")
        else:
            st.error("Invalid license key.")
