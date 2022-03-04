from flask import Blueprint,render_template,request,session,redirect

from mys10pro.utils.mypool import PoolDB
account = Blueprint('account',__name__)
from wtforms import Form,validators,widgets
#validators表示字符长度等的验证器，widgets是插件
from wtforms.fields import simple,html5,core
class LoginForm(Form):

    user = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空'),
            validators.Length(min=1,max=6,message='用户名必须大于%(min)d小于%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={'class':'form-control'},
        default='alex'
    )
    pwd = simple.StringField(
        label='密码',
        validators=[
            validators.DataRequired(message='请输入密码'),
            validators.Length(min=2,message='密码长度必须大于%(min)d'),
            # validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class':'form-control'}
    )

@account.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':

        form = LoginForm()
        print('进入get',form)
        # return "longin"
        return render_template('login.html',form=form)#居然要加参数名from=，默认的话会报错
    form = LoginForm(formdata=request.form)
    if not form.validate():  # validate提供一个类似校验的功能
        return render_template('login.html', form=form)
    sql = "SELECT * FROM `fl_user` WHERE username='%(user)s' AND pwd='%(pwd)s'"%(form.data)

    with PoolDB() as mycursor:
        mycursor.execute(sql)
        result = mycursor.fetchone()
    if result:
        session.permanent = True#允许修改嵌套的字典
        session['user_info'] = {'id':result['id'],'name':result['username']}
        return redirect('/index')
    else:
        return render_template('login.html',form=form)

class Register(Form):

    user = simple.StringField(
        label='用户名',
        validators=[
            validators.DataRequired(message='用户名不能为空'),
            validators.Length(min=1,max=6,message='用户名必须大于%(min)d小于%(max)d')
        ],
        widget=widgets.TextInput(),
        render_kw={'class':'form-control'},
        default='alex'
    )
    pwd = simple.StringField(
        label='密码',
        validators=[
            validators.DataRequired(message='请输入密码'),
            validators.Length(min=2,message='密码长度必须大于%(min)d'),
            # validators.Regexp(regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}",
            #                   message='密码至少8个字符，至少1个大写字母，1个小写字母，1个数字和1个特殊字符')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class':'form-control'}
    )
    pwd_confirm = simple.PasswordField(
        label='重复密码',
        validators=[
            validators.DataRequired(message='密码不能为空'),
            validators.EqualTo('pwd',message="两次输入的密码不一致")
        ],#EqualTo比较两个字段
        widget=widgets.PasswordInput(),
        render_kw={'class':'form-control'}
    )
    email = html5.EmailField(
        label='邮箱',
        validators=[
            validators.DataRequired(message='邮箱不能为空'),
            validators.Email(message='邮箱格式错误')
        ],
        widget = widgets.TextInput(input_type='email'),
        render_kw={'class': 'form-control'}
    )
    gender = core.RadioField(
        label='性别',
        choices=(
            (1,'男'),
            (2,'女'),
        ),
        coerce=int#coerce把choices的值转换成int
    )
    city = core.SelectField(
        label='城市',
        choices=(
            (1, '广州'),
            (2, '深圳'),
        ),
        coerce=int
    )
    hobby = core.SelectMultipleField(
        label='爱好',
        choices=(
            (1, '篮球'),
            (2, '足球'),
        ),
        coerce=int
    )
    favor = core.SelectMultipleField(
        label='喜好',
        choices=(
            (1, '唱歌'),
            (2, '跳舞'),
        ),
        widget=widgets.ListWidget(prefix_label=False),
        option_widget=widgets.CheckboxInput(),#默认多选
        coerce=int,
        default=[1, 2]
    )
    # def __init__(self,*args,**kwargs):
    #     super(Register,self).__init__(*args,**kwargs)
    #     self.city.choices=get_data()
        #重写父类的构造方法，使得每次实例化都会刷新一次city方法!!!
@account.route('/register',methods=['GET','POST'])

def register():
    if request.method =='GET':
        form = Register()
        return render_template('register.html',form=form)
    form = Register(formdata=request.form)
    if form.validate():
        print('获取注册信息',form.data)
        #存入数据库
        sql = "INSERT INTO `fl_user`(`username`, `pwd`) VALUES ('%(user)s','%(pwd)s')"%(form.data)
        with PoolDB() as mycorsur:
            mycorsur.execute(sql)

    else:
        print(form.errors)
    return redirect('/login')
