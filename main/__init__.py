from flask import Flask
from os import path
from keras.models import load_model
from joblib import load


app = Flask(__name__)
app.config["SECRET_KEY"] = "secrsdf4565423{et"

model = load_model('./ML/alpha_pred.h5')
scaler = load('./ML/std_scaler.bin')

from main.views import views
app.register_blueprint(views, url_prefix="/")
