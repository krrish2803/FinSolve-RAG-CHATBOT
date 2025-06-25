import json

def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def authenticate_user(email, password):
    users = load_users()
    user = users.get(email)
    if user and user["password"] == password:
        return {"email": email, "role": user["role"]}
    return None
