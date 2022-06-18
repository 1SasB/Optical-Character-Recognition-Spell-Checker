from flask import Flask,Blueprint, render_template, session, request, redirect, url_for,jsonify,flash
from .alpha_extracter import pred_img
import os
import numpy as np
from . import alpha_model,alpha_scaler,num_model,num_scaler
from english_words import english_words_set
import difflib
UPLOAD_FOLDER = 'main/static/uploads/'
A_Z = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
NUMS = ['0','1','2','3','4','5','6','7','8','9']
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

views = Blueprint("views",__name__)

@views.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        print(request.form) 
        file = request.files["file"]
        
        try:

            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))

        except Exception as e:
            data ={
                "message": "failed"
            }
            print(e)
            return jsonify(data)   

        if request.form['select-op'] == 'alpha':

            nm = pred_img(file.filename)
            word = predict(nm,alpha_scaler,alpha_model,A_Z)
            checked = check_spelling(word)

            data = org_data(checked,word,file.filename)
            return jsonify(data)
            
        else:
            nm = pred_img(file.filename)
            word = predict(nm,num_scaler,num_model,NUMS)

            data ={
                "file":file.filename,
                "message": "success",
                "word": word
            }
            return jsonify(data)

    return render_template('home.html')


def org_data(d,w,f):
    if d == w:
        data ={
            "file":f,
            "message": "success",
            "word": w
        }
    else:
        data ={
            "similar_words": d,
            "file":f,
            "message": "success",
            "word": w
        }
    return data


def predict(n_images,scaler,model,scope):
     


    # scaler=load('std_scaler.bin')
    new_images = scaler.transform(n_images)

    predictions = [ np.argmax(np.array(list(map(int,pred == max(pred))))) for pred in model.predict(new_images)]
    predictions = [scope[p] for p in predictions]
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
