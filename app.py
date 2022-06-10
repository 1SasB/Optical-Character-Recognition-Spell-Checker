from flask import Flask, render_template, session, request, redirect, url_for,jsonify,flash

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True, port=5000)