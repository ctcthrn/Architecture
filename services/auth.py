from flask import Flask, request, jsonify

app = Flask(__name__)

# база пользователей (логин: пароль)
users = {
    "user1": "qwerty",
    "user2": "12345",
    "user3": "67890",
}

@app.route("/auth", methods=["POST"])
def auth():
    data = request.get_json() # получение данных из POST запроса
    if not data or "login" not in data or "password" not in data:
        return jsonify({"allowed": False}), 400 # если некорректно, то false bad request 400

    login = data["login"]
    password = data["password"]

    allowed = users.get(login) == password
    return jsonify({"allowed": allowed})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008, debug=True)