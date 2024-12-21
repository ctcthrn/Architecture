from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.get_json() # получение данных из POST запроса
    if not data or "login" not in data:
        return jsonify({"error": "Invalid request"}), 400 # если некорректно, то false bad request 400
    score_value = random.random() # рандомный скоринг от 0 до 1
    return jsonify({"score": score_value})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7007, debug=True)
