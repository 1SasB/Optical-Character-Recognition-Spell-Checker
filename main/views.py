from flask import Flask,Blueprint, request,jsonify
import numpy as np
from . import alpha_model,alpha_scaler,num_model,num_scaler
# from english_words import english_words_set
import difflib

A_Z = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
NUMS = ['0','1','2','3','4','5','6','7','8','9']

app = Flask(__name__)

views = Blueprint("views",__name__)

@views.route("/predict", methods=["POST"])
def index():
    data = request.json
    arr = np.array(data['arr'])
    if data['type'] == 'alpha':

        print(arr,arr.shape)
        word = predict(arr,alpha_scaler,alpha_model,A_Z)
        data = {
            "message":"success",
            "word": word
        }
        return jsonify(data)
    else:
        print(arr,arr.shape)
        word = predict(arr,num_scaler,num_model,NUMS)
        data = {
            "message":"success",
            "word": word
        }
        return jsonify(data)




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

# def check_spelling(pword):
#   if(pword in english_words_set):
#     print(f"Recognised word: {pword}")
#     return pword
#   else:
#     close_matches = difflib.get_close_matches(pword, english_words_set)
#     print(f"Sorry we are unable to recognise your word,\nDid you mean any of these:  {close_matches}")
#     return close_matches
