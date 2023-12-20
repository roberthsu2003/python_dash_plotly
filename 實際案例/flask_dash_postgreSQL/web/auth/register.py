from flask import Blueprint, render_template, abort,redirect,request,session
from jinja2 import TemplateNotFound
from flask_wtf import FlaskForm
from wtforms import PasswordField,EmailField,StringField,SelectField,BooleanField,DateField,TextAreaField
from wtforms.validators import DataRequired,Length,Regexp,Optional,EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
from .datasource import insert_data,validateUser,InvalidEmailException
from . import password as pw
import secrets
import datetime

register_blue = Blueprint('register',__name__,url_prefix='/auth')

class UserRegistrationForm(FlaskForm):
    uName = StringField("姓名",validators=[DataRequired(),Length(min=2, max=10)])
    uGender = SelectField("性別", choices=[("男", "男"), ("女", "女"), ("其它","其它")])
    uPhone = StringField("聯絡電話",validators=[DataRequired(),Regexp(r'\d\d\d\d-\d\d\d-\d\d\d',message="格式不正確")])
    uEmail = EmailField("電子郵件",validators=[DataRequired()])
    isGetEmail = BooleanField("接受促銷email",default=False)
    uBirthday = DateField("出生年月日",validators=[Optional()],format='%Y-%m-%d')
    uAboutMe = TextAreaField('自我介紹', validators=[Optional(), Length(max=200)],description='最多200字')
    uPass = PasswordField("密碼",validators=[DataRequired(),Length(min=4, max=20),EqualTo('uConfirmPass',message="驗証密碼不正確")])
    uConfirmPass = PasswordField("驗証密碼",validators=[DataRequired(),Length(min=4, max=20)])

@register_blue.route("/register",methods=['GET','POST'])
def register():
    form = UserRegistrationForm()
    if request.method == "POST":
        print("post")
        if form.validate_on_submit():
            uName = request.form['uName']
            print("姓名=",uName)

            uGender = form.uGender.data
            print("性別=",uGender)            

            uPhone = form.uPhone.data
            print("電話=",uPhone)

            uEmail = form.uEmail.data
            #form.uEmail.errors.append("email有相同的") #自訂錯誤
            print("email=",uEmail)

            isGetEmail = form.isGetEmail.data
            print("促銷=", "接受" if isGetEmail else "不接受" )

            uBirthday:datetime.date | None = form.uBirthday.data
            #uBirthday型別是datetime.date
            if uBirthday is not None:
                uBirthday_str = uBirthday.strftime("%Y-%m-%d")
                print("出生年月日:",uBirthday_str)
            else:
                uBirthday_str = "1900-01-01"

            uAboutMe = form.uAboutMe.data #沒有填是空字串
            print("關於我:",uAboutMe) 

            uPass = form.uPass.data
            print("密碼:",uPass)

                      
            #產生password hash
            hash_password= generate_password_hash(uPass,method='pbkdf2:sha256',salt_length=8)

            conn_token = secrets.token_hex(16)                
            try:
                insert_data([uName,uGender,uPhone,uEmail,isGetEmail,uBirthday_str,uAboutMe,hash_password,conn_token])

            except InvalidEmailException:
                form.uEmail.errors.append("有相同的email") #自訂錯誤
            except:
                form.uEmail.errors.append("不知名的錯誤")
            else:
                return redirect(f'/auth/login/{uEmail}')         
        else:
            print("驗證失敗")
    else:
        print("第一次進入")
    return render_template("auth/register.html",form=form)



class MyForm(FlaskForm):
    email = EmailField('郵件信箱',validators=[DataRequired()])
    password = PasswordField('密碼',validators=[DataRequired(),Length(min=4,max=20)])    

@register_blue.route("/login",methods=['GET','POST'])
@register_blue.route("/login/<email>",methods=['GET'])
def login(email:str | None = None):
    form = MyForm()
    if request.method == "POST":
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            is_ok, name= validateUser(email,password) #驗証ok,傳出tuple
            if is_ok:
                session['username'] = name #將使用者名稱加入至username內
                return redirect("/")
            else:                
                form.email.errors.append("帳號或密碼錯誤")
                form.email.data = ""               
        else:
            print("驗證失敗")      
        
    else:
        print("第一次進入")
        if email is not None:
            form.email.data = email           

    return render_template("auth/login.html",form = form)

@register_blue.route('/success')
def success():
    return render_template('auth/success.html')

@register_blue.route('/logout')
def logout():
    session.pop('username',default=None)
    return redirect('/')