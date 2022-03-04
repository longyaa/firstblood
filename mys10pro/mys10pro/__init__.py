from flask import Flask
from .views import account

from flask_session import Session
from flask_uploads import UploadSet,configure_uploads,DOCUMENTS
import os

myfile = UploadSet('myfile', DOCUMENTS)
def create_app():
    app = Flask(__name__)
    app.config.from_object('settings.DevelopmentConfig')

    app.register_blueprint(account.account)
    app.config['UPLOADED_MYFILE_DEST'] = os.getcwd()

    configure_uploads(app,myfile)
    from .views import home
    app.register_blueprint(home.home)
    Session(app)  # 替换session保存
    return app
