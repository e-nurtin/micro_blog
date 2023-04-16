from flask_login import current_user, login_required
from app import db
from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from datetime import datetime
from app.main.forms import EditProfileForm, EmptyForm, PostForm
from app.main import bp
from app.models import User, Post
from flask_babel import _, get_locale
from langdetect import detect, LangDetectException
from app.translate import translate


@bp.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()
		g.locale = str(get_locale())


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
@login_required
def index():
	form = PostForm()
	
	if form.validate_on_submit():
		try:
			language = detect(form.post.data)
		except LangDetectException:
			language = ''
		post = Post(body=form.post.data, author=current_user, language=language)
		
		db.session.add(post)
		db.session.commit()
		flash(_("Post is shared successfully!"))
		return redirect(url_for('main.index'))
	
	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(
		page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	next_url = url_for('main.index', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.index', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', title='Home Page',
	                       posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
	user_ = User.query.filter_by(username=username).first_or_404()
	form = EmptyForm()
	page = request.args.get('page', 1, type=int)
	posts = user_.posts.order_by(Post.timestamp.desc()).paginate(
		page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	next_url = url_for('main.user', username=user_.username, page=posts.next_num) if posts.has_next else '#'
	prev_url = url_for('main.user', username=user_.username, page=posts.prev_num) if posts.has_prev else '#'
	return render_template('user.html', user=user_, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash(_('Your changes have been saved!'))
		return redirect(url_for('main.edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	
	return render_template('edit_profile.html', title="Edit Profile", form=form)


@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
	form = EmptyForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		
		if user is None:
			flash(_(f"User {username} is not found!"))
			return redirect(url_for('main.index'))
		
		if user == current_user:
			flash(_("You cannot follow yourself!"))
			return redirect(url_for('main.user', username=username))
		
		current_user.follow(user)
		db.session.commit()
		flash(_(f'You are now following {username}!'))
		return redirect(url_for('main.user', username=username))
	else:
		return redirect(url_for('main.index'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
	form = EmptyForm()
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=username).first()
		
		if user is None:
			flash(_(f"User {username} is not found!"))
			return redirect(url_for('main.index'))
		
		if user == current_user:
			flash(_("You cannot unfollow yourself!"))
			return redirect(url_for('main.user', username=username))
		
		current_user.unfollow(user)
		db.session.commit()
		flash(_(f'You are not following {username} anymore!'))
		return redirect(url_for('main.user', username=username))
	else:
		return redirect(url_for('main.index'))


@bp.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.timestamp.desc()).paginate(
		page=page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
	next_url = url_for('main.explore', page=posts.next_num) if posts.has_next else None
	prev_url = url_for('main.explore', page=posts.prev_num) if posts.has_prev else None
	return render_template('index.html', posts=posts.items,
	                       next_url=next_url, prev_url=prev_url, page=page)


@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
	return jsonify({'text': translate(request.form['text'],
	                                  request.form['source_language'],
	                                  request.form['dest_language'])})
