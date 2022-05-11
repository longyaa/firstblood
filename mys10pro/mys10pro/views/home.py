
from ..utils.mypool import PoolDB

import pandas as pd
from flask import Blueprint,render_template
from flask_uploads import patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms import SubmitField
from .. import myfile

home = Blueprint('home',__name__)

class UploadedForm(FlaskForm):
    photo = FileField(validators=[
        FileAllowed(myfile,u'只能上传xls！'),
        FileRequired(u'文件未选择!')
    ])
    submit = SubmitField(u'上传')
@home.route('/index')
def index():
    form = UploadedForm()
    if form.validate_on_submit():
        filename = myfile.save(form.photo.data)
        file_url = myfile.url(filename)

        df = pd.read_excel(file_url,header=0).fillna(0)
        df2 = df.to_dict(orient = 'records')

        mydata = []
        for i in df2:
            mydata.append((i['name'],i['pwd']))
        sql1 = 'insert into fl_user(`username`,`pwd`) values (%s,%s)'
        with PoolDB() as mycorsur2:
            mycorsur2.executemany(sql1,mydata)
    else:
        file_url = None
    # 读出数据
    sql2 = "SELECT username,pwd FROM `fl_user`"
    with PoolDB() as mycorsur:
        mycorsur.execute(sql2)
        result2 = mycorsur.fetchall()
    return render_template('index.html',form=form,file_url=file_url,info=result2)
