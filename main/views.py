from flask import Flask,Blueprint, render_template, session, request, redirect, url_for,jsonify,flash
from .alpha_extracter import pred_img
import os
import numpy as np
from . import model,scaler
from english_words import english_words_set
import difflib
UPLOAD_FOLDER = 'main/static/uploads/'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint("views",__name__)

@views.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":

        file = request.files["file"]
        
        try:

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))

            nm = pred_img(file.filename)
            word = predict_word(nm)
            checked = check_spelling(word)

            if checked == word:

                data ={
                    "file":file.filename,
                    "message": "success",
                    "word": word
                }
            else:
                data ={
                    "similar_words": checked,
                    "file":file.filename,
                    "message": "success",
                    "word": word
                }
        except Exception as e:
            data ={
                "message": "failed"
            }
            print(e)
        return jsonify(data)    
    return render_template('home.html')




def predict_word(n_images):
    A_Z = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'] 


    # scaler=load('std_scaler.bin')
    new_images = scaler.transform(n_images)

    predictions = [ np.argmax(np.array(list(map(int,pred == max(pred))))) for pred in model.predict(new_images)]
    predictions = [A_Z[p] for p in predictions]
    print(predictions) 
    predicted_word = "".join(predictions)
    predicted_word = predicted_word.lower()

    print(predicted_word)
    return predicted_word

def check_spelling(pword):
  if(pword in english_words_set):
    print(f"Recognised word: {pword}")
    return pword
  else:
    close_matches = difflib.get_close_matches(pword, english_words_set)
    print(f"Sorry we are unable to recognise your word,\nDid you mean any of these:  {close_matches}")
    return close_matches
