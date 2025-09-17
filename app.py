from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(ok=True, message="Hola Flask en WSL 🚀")

if __name__ == "__main__":
    # Para ejecución directa: python3 app.py
    app.run(debug=True, host="0.0.0.0", port=5000)
