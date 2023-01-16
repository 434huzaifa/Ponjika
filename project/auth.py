from flask import Blueprint, render_template, request, url_for, redirect, jsonify,make_response,current_app
from .models import User
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import login_user, logout_user,current_user
from flask_uploads import UploadSet, IMAGES
import requests
from werkzeug.datastructures import  FileStorage
import io
auth = Blueprint('auth', __name__)

photos = UploadSet('images', IMAGES)

@auth.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']

        password=request.form['password']
        remember=request.form['remember']
        print(email)
        user=User.objects(email=email).first()
        print(user)
        if user:
            if check_password_hash(user.password,password):
                if remember=='true':
                    login_user(user,remember=True)
                else:
                    login_user(user)
                response={'message':'valid user','error':False}
                return make_response(response,200)
            else:
                response={'message':'wrong password','error':True}
                return make_response(response,200)
        else:
            response={'message':'invalid user','error':True}
            return make_response(response,200)
    return render_template('login.html')
@auth.route('/signup/',methods=['POST'])
def signup():
    if request.method=='POST':
        print(request.form)
        name=request.form['name']
        username=request.form['username']
        email=request.form['email']
        password1=request.form['password1']
        password2=request.form['password2']
        user=User.objects(email=email).first()
        if not user:
            if password1==password2:
                cipher=generate_password_hash(password1)
               
                user=User(name=name,username=username,email=email,password=cipher)
                user.save()
            
                img_url="https://api.multiavatar.com/"+username+".png"
                res=requests.get(img_url,allow_redirects=True)
                if res.ok:
                    print('res')
                    filename=str(user.id)+'.png'
                    f=FileStorage(io.BytesIO(res.content),filename=filename)
                    f=photos.save(f,folder=str(user.id))
                    user.update(set__image=f)
                response={'message':'valid user','error':False}
                return make_response(response,200)
            else:
                response={'message':'Passoword Not Match','error':True}
                return make_response(response,200)
        else:
            response={'message':'User Exist','error':True}
            return make_response(response,200)
    return render_template('login.html')

@auth.route('/logout/')
def logouut():
    logout_user()
    return redirect('/login/')


