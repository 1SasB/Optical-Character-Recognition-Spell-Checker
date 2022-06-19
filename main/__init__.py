from flask import Flask
from os import path
from keras.models import load_model
from joblib import load


app = Flask(__name__)
app.config["SECRET_KEY"] = "secrsdf4565423{et"

alpha_model = load_model('./ML/alpha_pred copy.h5')
alpha_scaler = load('./ML/std_scaler copy.bin')

num_model = load_model('./ML/numeric_pred.h5')
num_scaler = load('./ML/num_std_scaler.bin')

from main.views import views
app.register_blueprint(views, url_prefix="/")
