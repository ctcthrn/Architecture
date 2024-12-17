from flask import Flask, request, jsonify

app = Flask(__name__)

# База пользователей (логин: пароль)
users = {
    "user1": "qwerty",
    "user2": "12345",
    "user3": "67890",
}

@app.route("/auth", methods=["POST"])
def authenticate_user():
    data = request.get_json()

    if not data or "login" not in data or "password" not in data:
        return jsonify({"allowed": False, "message": "Login and password are required."}), 400

    login = data["login"]
    password = data["password"]

    user_data = users.get(login)
    if user_data is None:
        return jsonify({"allowed": False, "message": "User not found."}), 404

    allowed = user_data == password
    return jsonify({"allowed": allowed, "message": "Authentication successful" if allowed else "Incorrect password."}), 200 if allowed else 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)
