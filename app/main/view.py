# -*- coding: utf-8 -*-
from flask import render_template,redirect,url_for,session,flash,\
     request, make_response, jsonify
from flask_login import login_required, current_user, current_app
from . import main
from .forms import NameForm, EditProfileForm, EditProfileAdminForm, CreateQuestion,\
    AnswerForm

from .. import db
from ..decorators import admin_required, permission_required
from ..models import Answer, User, Question, Role, Permission

import json
@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp


@main.route('/followed')
@login_required
def show_followed():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '1', max_age=30*24*60*60)
    return resp

@main.route('/welcome',methods=['GET', 'POST'])
def welcome():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash(u"老哥，看来你把名字改了啊，技术不错！")
        session['name'] = form.name.data
        return redirect(url_for('main.welcome'))
    return render_template('welcome.html', form=form, name=session.get('name'))


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    #page = request.args.get('page', 1, type=int)
    #pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
    #    page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
    #    error_out=False)
    #posts = pagination.items
    #return render_template('user.html', user=user, posts=posts,
    #                       pagination=pagination)
    return render_template('user.html',user=user)

@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'你的修改已经提交')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'用户已经更新')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/', methods=['GET'])
def index():
    return render_template('vuedemo.html')

@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在')
        return redirect(url_for('.index'))
    if current_user.is_following(user):
        flash(u'你已经关注该用户.')
        return redirect(url_for('.user', username=username))
    current_user.follow(user)
    flash(u'关注%s成功。' % username)
    return redirect(url_for('.user', username=username))


@main.route('/unfollow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在.')
        return redirect(url_for('.index'))
    if not current_user.is_following(user):
        flash(u'已经取关')
        return redirect(url_for('.user', username=username))
    current_user.unfollow(user)
    flash(u'你已经取关 %s ' % username)
    return redirect(url_for('.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followers of",
                           endpoint='.followers', pagination=pagination,
                           follows=follows)


@main.route('/followed-by/<username>')
def followed_by(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'用户不存在.')
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', user=user, title="Followed by",
                           endpoint='.followed_by', pagination=pagination,
                           follows=follows)

@main.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Question.query.filter_by(id=id).first_or_404()
    form = AnswerForm()
    if form.validate_on_submit():
        answer = Answer(body=form.body.data,
                          question=Question.query.filter_by(id),
                          author=current_user._get_current_object())
        db.session.add(answer)
        flash(u'你的回答已经提交')
        return redirect(url_for('.post', id=id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.ansnwer.count() - 1) // \
            current_app.config['FLASKY_COMMENTS_PER_PAGE'] + 1
    pagination = post.answer.order_by(Answer.timestamp.asc()).paginate(
        page, per_page=current_app.config['FLASKY_COMMENTS_PER_PAGE'],
        error_out=False)
    answers = pagination.items
    return render_template('post.html', question=post, posts=[post], form=form,
                           answers=answers, pagination=pagination)

@main.route('/trick', methods=['GET', ])
def trick():
    return render_template('trick.html')

@main.route('/qindex', methods=['GET', ])
def qindex():
    return render_template('qindex.html')

@main.route('/qsource', methods=['GET', ])
def qsource():
    return render_template('qsource.html')

@main.route('/gaohu', methods=['GET', ])
def gaohu():
    return render_template('gaohu.html')

@main.route('/gaohuapi', methods=['GET', ])
def answerjson():
    user = User.query.filter_by(id =3).first()
    answers = db.session.query(Answer.body.label('Ansbody'),Question.body.label('Qbody'),User.username) \
    .filter(Answer.author_id == 3).filter(User.id == Answer.author_id).filter(Question.id == Answer.Question_id).all()
    as_dict = [answer._asdict() for answer in answers]
    jsonlist = json.dumps(as_dict,ensure_ascii=False).encode('utf8')
    jsonlist= jsonify(jsonlist)
    jsonlist.headers.add('Access-Control-Allow-Origin', '*')
    return jsonlist

