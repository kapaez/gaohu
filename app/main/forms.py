# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, \
    SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField

class NameForm(FlaskForm):
    name = StringField(u'你的名字是？', validators=[Required()])
    submit = SubmitField(u'提交')


class EditProfileForm(FlaskForm):
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个性签名')
    submit = SubmitField(u'提交')

class EditProfileAdminForm(FlaskForm):
    email = StringField(u'邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField(u'用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          u'用户名只能用英文数字以及._')])
    confirmed = BooleanField(u'验证状态')
    role = SelectField(u'权限', coerce=int)
    name = StringField(u'真实姓名', validators=[Length(0, 64)])
    location = StringField(u'地址', validators=[Length(0, 64)])
    about_me = TextAreaField(u'个性签名')
    submit = SubmitField(u'确认')

class CreateQuestion(FlaskForm):
    discribt = StringField(u'你想问什么问题？', validators=[Length(0, 128)])
    submit = SubmitField(u'提问')

class AnswerForm(FlaskForm):
    body = StringField(u'你的回答是什么？', validators=[Length(0, 500)])
    submit = SubmitField(u'提交')