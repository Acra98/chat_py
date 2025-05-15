from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, send
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        if username:
            session["username"] = username
            return redirect(url_for("chat"))
    return render_template("login.html")

@app.route("/chat")
def chat():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("chat.html", username=session["username"])

@socketio.on("message")
def handle_message(msg):
    send(msg, broadcast=True  )

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=6020, debug=True, allow_unsafe_werkzeug=True)