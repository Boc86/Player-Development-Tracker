import hydralit as hy
import supabase
import hashlib
import re
from datetime import date

supabase_url = hy.secrets["supabase_url"]
supabase_key = hy.secrets["supabase_key"]
supabase_client = supabase.create_client(supabase_url, supabase_key)

def validate_username(username):
    """Check for duplicate username"""
    response = supabase_client.table("user").select("email").eq("email", username).execute()
    res = " " in username

    try:
        if res:
            hy.error("Username cannot contain spaces")
            return False

        if response.data:
            hy.error("Email already in use, please choose a different one")
            return False
    except Exception as e:
        hy.error(f"Login error: {e}")

    return True

def hash_password(password):
    """Simple password hashing function."""
    return hashlib.sha256(password.encode()).hexdigest()

def validate_email(email):
    """
    Validate email format with more comprehensive regex.
    
    Checks for:
    - One or more characters before the @
    - A domain name after @
    - A top-level domain of 2-4 characters
    - Allows for valid special characters in local part
    """
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    
    # Additional specific checks
    if not re.match(email_regex, email):
        return False
    
    # Ensure no consecutive dots in local part
    if '..' in email.split('@')[0]:
        return False
    
    # Ensure domain has at least one dot
    domain = email.split('@')[1]
    if '.' not in domain:
        return False
    
    return True

def check_login(username, password):
    """Check user credentials against Supabase."""

    hashed_password = hash_password(password)
    
    try:
        # Fetch user from Supabase
        response = supabase_client.table("user").select("*").eq("email", username).execute()
        
        if response.data:
            # Compare hashed passwords
            stored_user = response.data[0]
            return stored_user["password_hash"] == hashed_password
    except Exception as e:
        hy.error(f"Login error: {e}")
        return False

def register_user(email, first_name, sur_name, password):
    role_id = 5

    try:
        # Check if info already exists
        existing_email = supabase_client.table("user").select("*").eq("email", email).execute()
        if existing_email.data:
            hy.error("Email already in use")
            return False

        # Hash the password
        hashed_password = hash_password(password)
        
        supabase_client.table("user").insert({
            "email": email,
            "first_name": first_name,
            "sur_name": sur_name,
            "password_hash": hashed_password,
            "role_id": role_id
        }).execute()
        return True
    except Exception as e:
        hy.error(f"Registration error: {e}")
        return False

def login_form():

    with hy.form(key="Login"):

        """Streamlit login page."""
        hy.title("KRFC Player Development Tracker")
        
        # Create tabs
        tab1, tab2 = hy.tabs(["Login", "Register"])
        
        with tab1:
            hy.header("Login")
            login_email = hy.text_input("Email", key="login_email")
            login_password = hy.text_input("Password", type="password", key="login_password")
            login_button: bool = hy.form_submit_button(label="Login")
            
            if login_button:
                if check_login(login_email, login_password):
                    # Store login state
                    hy.session_state['logged_in'] = True
                    hy.session_state['email'] = login_email

                    response = supabase_client.table("user").select("first_name, role_id, id").eq("email", login_email).execute()
                    if response.data:
                        hy.session_state['first_name'] = response.data[0]["first_name"]
                        hy.session_state['role'] = str(response.data[0]["role_id"])
                        hy.session_state['user_id'] = response.data[0]["id"]

                    hy.rerun()
                    
                else:
                    hy.error("Invalid username or password")
        
        with tab2:
            hy.header("Register")
            # Registration form with added fields
            reg_email = hy.text_input("Email Address", key="reg_email")
            reg_first_name = hy.text_input("First Name", key="reg_first_name")
            reg_sur_name = hy.text_input("Surname", key="reg_sur_name")
            reg_password = hy.text_input("Create a Password", type="password", key="reg_password")
            confirm_password = hy.text_input("Confirm Password", type="password", key="confirm_password")
            register_button: bool = hy.form_submit_button(label="Register")
            
            if register_button:
                # Comprehensive validation
                validation_errors = []
            
                # Email validation
                if not validate_email(reg_email):
                    validation_errors.append("Invalid email address format")
                
                # Password validations
                if len(reg_password) < 6:
                    validation_errors.append("Password must be at least 6 characters long")
                
                if reg_password != confirm_password:
                    validation_errors.append("Passwords do not match")

                # Display or proceed with registration
                if validation_errors:
                    for error in validation_errors:
                        hy.error(error)
                else:
                    # Attempt registration
                    if register_user(reg_email, reg_first_name, reg_sur_name, reg_password):
                        hy.success("Registration successful! You can now log in.")