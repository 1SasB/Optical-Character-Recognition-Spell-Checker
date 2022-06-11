from flask import Flask, render_template, session, request, redirect, url_for,jsonify,flash
from .ML import alpha_extracter
import os
UPLOAD_FOLDER = 'static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def index():    
    return render_template('home.html')

@app.route("/upload-file", methods=["POST"])
def upload_image():
    if request.method == "POST":
        print("here")
        file = request.files["file"]
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
        # word = alpha_extracter.pred_img(file.filename)
        # print(word)
        data ={
            "file":file.filename,
            "message": "success"
        }
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)