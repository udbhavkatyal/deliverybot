from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Discord bot is running!"

@app.route("/health")
def health():
    return {"status": "ok"}, 200

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    Thread(target=run, daemon=True).start()