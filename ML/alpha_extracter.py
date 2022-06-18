import numpy as np
import cv2
# import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import load_model

from joblib import load
from english_words import english_words_set
import difflib


# file_path = "../static/uploads/"+filename
image = cv2.imread('word4.jpg')
im = image.copy()
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

imgray = imgray.flatten()

with_contours = cv2.drawContours(im, contours, -1, (0,255,0), 3)

new_images = []
for hr,c in zip(hierarchy[0],contours):
  x, y, w, h = cv2.boundingRect(c)

  # Make sure contour area is large enough
if hr[3]==0 and (cv2.contourArea(c)) > 9000:
  cv2.rectangle(with_contours,(x,y), (x+w,y+h), (255,0,0), 5)
  alpha_im = image[y:(y+h),x:(x+w)]
  alpha_im = cv2.cvtColor(alpha_im, cv2.COLOR_BGR2GRAY)
  alpha_im = cv2.bitwise_not(alpha_im)
  alpha_im = cv2.copyMakeBorder(alpha_im,100,100,100,100,cv2.BORDER_CONSTANT)
  alpha_im = cv2.resize(alpha_im, (28,28)).flatten()
  
  print(alpha_im.shape)
  new_images.append(alpha_im)

new_images = np.array(new_images)


A_Z = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
model = load_model("alpha_pred.h5")


scaler=load('std_scaler.bin')
new_images = scaler.transform(new_images)

predictions = [ np.argmax(np.array(list(map(int,pred == max(pred))))) for pred in model.predict(new_images)]
predictions = [A_Z[p] for p in predictions]

predicted_word = "".join(predictions)
predicted_word = predicted_word.lower()

print(predicted_word)



if(predicted_word in english_words_set):
  print(f"Recognised word: {predicted_word}")
else:
  close_matches = difflib.get_close_matches(predicted_word, english_words_set)
  print(f"Sorry we are unable to recognise your word,\nDid you mean any of these:  {close_matches}")
