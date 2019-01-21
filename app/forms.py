from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, validators
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import *


class RegisterForm(FlaskForm):
    studentid = StringField(label='学号', description='学号',
                            validators=[DataRequired(u"请输入学号"), Length(9, 10, message=u'请输入正确的学号格式')])
    username = StringField(label='用户名', description='用户名长度为3-15个字符',
                           validators=[DataRequired(u"请输入用户名"), Length(3, 15, message=u'请输入正确的用户名格式')])
    description = StringField(label='备注', description='请输入备注信息方便管理员认证',
                              validators=[DataRequired(u'备注信息不能为空'), Length(3, 100)])
    password = PasswordField(label='密码', description='密码长度为5-20个字符',
                             validators=[DataRequired(u"密码不能为空"), Length(5, 20, message=u'密码长度不正确')])
    confirm = PasswordField(label='再次输入密码', description='再次输入密码', validators=[DataRequired(u"密码不能为空"),
                                                                              EqualTo('password', message=u"两次密码必须一致")])

    submit = SubmitField(label='注册')


'''
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'该用户名已被注册，请更换')
'''


class LoginForm(FlaskForm):
    # studentid = StringField(label='学号', description='请输入您的学号', validators=[DataRequired("请输入您的学号"), Length(9, 10, message=u'请输入正确的学号格式')])
    username = StringField(label='用户名', description='请输入用户名', validators=[DataRequired(u"用户名不能为空")])
    password = PasswordField(label='密码', description='请输入密码', validators=[DataRequired(u"密码不能为空")])
    submit = SubmitField(label='登录')
