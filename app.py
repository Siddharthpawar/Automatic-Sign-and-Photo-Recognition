from flask import Flask, render_template, request
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np

app = Flask(__name__)

model = load_model('predimg.h5')
photo_pred = ''
sign_pred = ''
photo_img = ''
sign_img = ''

@app.route('/',methods=['GET','POST'])
def hello():
    global photo_img,photo_pred,sign_img,sign_pred
    photo_pred = ''
    sign_pred = ''
    photo_img = ''
    sign_img = ''
    return render_template('index2.html',prediction1='', prediction2='', img_p='', img_s='')

@app.route('/photograph',methods=['POST','GET'])
def predict():
    if(request.method=='GET'):
        print(request.form.get('reset-form'))
    global photo_pred, photo_img
    if(request.method=='PUT'):
        return render_template('index2.html', prediction1="", prediction2=sign_pred, img_p="", img_s=sign_img)
    imagefile = request.files['imagefile']
    print(imagefile)
    #image_path = "./images/" + imagefile.filename
    image_path = "./static/images/" + imagefile.filename
    imagefile.save(image_path)

    image = load_img(image_path, target_size=(150,150))
    image = img_to_array(image)
    image = np.expand_dims(image,axis=0)
    val = model.predict(image)
    if val > 0.5:
        print('Sign')
        classification = 'Sign'
    else:
        print('Photograph')
        classification = 'Photograph'

    photo_pred=classification
    photo_img=image_path
    print('*',request.form.get("hidden_button"),'*')
    
    #return render_template('index2.html', prediction1=photo_pred, prediction2=sign_pred, img_p=request.form.get("hidden_button"))
    return render_template('index2.html', prediction1=photo_pred, prediction2=sign_pred, img_p=photo_img, img_s=sign_img)

@app.route('/sign',methods=['POST'])
def predict1():
    imagefile = request.files['imagefile']
    #image_path = "./images/" + imagefile.filename
    image_path = "./static/images/" + imagefile.filename
    imagefile.save(image_path)

    image = load_img(image_path, target_size=(150,150))
    image = img_to_array(image)
    image = np.expand_dims(image,axis=0)
    val = model.predict(image)
    if val > 0.5:
        print('Sign')
        classification = 'Sign'
    else:
        print('Photograph')
        classification = 'Photograph'

    global sign_pred, sign_img
    sign_pred=classification
    sign_img=image_path
    return render_template('index2.html', prediction1=photo_pred ,prediction2=sign_pred, img_p=photo_img, img_s=sign_img)



if __name__ == '__main__':
    app.run(port=3000, debug=True)