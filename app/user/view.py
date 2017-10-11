# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from ..email import send_email
from .forms import LoginForm, RegisterForm, PasswordResetRequestForm, ChangePasswordForm, \
    ChangeEmailForm, PasswordResetForm

from . import user
from .. import db
from ..models import User

@user.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != 'user.' \
                and request.endpoint != 'static':
            return redirect(url_for('user.unconfirmed'))

#请求验证路由
@user.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('user/unconfirmed.html')


#登录路由
@user.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        users = User.query.filter_by(email=form.email.data).first()
        if users is not None and users.verify_password(form.password.data):
            login_user(users, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash(u'用户名或者密码错误')
    return render_template('user/login.html', form=form)

@user.route('/register',methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        users = User.query.filter_by(username=form.username.data).first()
        if users == None:
            users = User(email=form.email.data,
                        username=form.username.data,
                        password=form.password.data,)
            db.session.add(users)
            db.session.commit()
            token = users.generate_confirmation_token()
            send_email(users.email, 'Confirm Your Account',
                       'user/email/confirm', user=users, token=token)
            flash(u'注册成功，验证邮件已经发送到你的邮箱，请及时确认。')
            return redirect(url_for('main.welcome'))
        else:
            flash(u'该用户被注册了，歹势')
            return redirect(url_for('user.register'))
    return render_template('user/registation.html',form=form)

#验证用户
@user.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash(u'你的账户已经验证成功！')
    else:
        flash(u'该验证链接有误')
    return redirect(url_for('main.index'))

#修改密码
@user.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash(u'你的密码已经更新.')
            return redirect(url_for('main.index'))
        else:
            flash(u'原密码不正确.')
    return render_template("user/change_password.html", form=form)


#再次发送验证邮件
@user.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'验证你的账户',
               'user/email/confirm', user=current_user, token=token)
    flash(u'一封新的邮件已经发送到你的账户')
    return redirect(url_for('main.index'))

#重设密码请求
@user.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        users = User.query.filter_by(email=form.email.data).first()
        if users:
            token = users.generate_reset_token()
            send_email(users.email, u'修改密码',
                       'user/email/reset_password',
                       user=users, token=token,
                       next=request.args.get('next'))
        flash(u'一封邮件已经发送到你的注册邮箱，点击邮件内链接重设密码')
        return redirect(url_for('user.login'))
    return render_template('user/reset_password.html', form=form)

#重设密码
@user.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        users = User.query.filter_by(email=form.email.data).first()
        if users is None:
            return redirect(url_for('main.index'))
        if users.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('user.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('user/reset_password.html', form=form)


@user.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, u'修改邮箱验证邮件',
                       'user/email/change_email',
                       user=current_user, token=token)
            flash(u'验证邮件已经发送至你的邮箱')
            return redirect(url_for('main.index'))
        else:
            flash(u'邮件地址或密码错误')
    return render_template("user/change_email.html", form=form)

@user.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash(u'修改成功！')
    else:
        flash(u'错误的请求')
    return redirect(url_for('main.index'))