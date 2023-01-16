from flask_uploads import UploadSet,configure_uploads,IMAGES
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
import os
db = MongoEngine()
photos=UploadSet('images',IMAGES)
def create_app():
    app=Flask(__name__)
    app.config['DEBUG'] = True
    app.config["MONGODB_SETTINGS"] = [
        {'db': 'database', 'host': 'localhost', 'port': 27017, 'alias': 'default'}]
    db.init_app(app)
    app.config['SECRET_KEY'] = 'KEY'
    app.config['UPLOADED_IMAGES_DEST'] = os.getcwd()+'\\project\\image' #THE CONFIG KEY WILL FIRST PARAMETER OF UPLOAD SET
    configure_uploads(app, (photos,))
    from .views import views
    from .auth import auth
    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    login_manager=LoginManager()
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        from .models import User
        return User.objects(id=str(id)).first()

    return app