from app import app
from flask import render_template, flash, redirect, url_for
from datetime import datetime
from app.forms import LoginForm


@app.route('/')
@app.route('/home')
def index():
	user = {'username': 'Ersin'}
	posts = [
		{
			'author': "Ersin Nurtin",
			'title': 'blog post 1',
			'post_description': 'Describing my interesting post1',
			'content': 'First post content',
			'date_posted': datetime.date(datetime.today())
		},
		{
			'author': "Ersin Nurtin",
			'title': 'blog post 2',
			'post_description': 'Describing my interesting post2',
			'content': 'Second post content',
			'date_posted': datetime.date(datetime.today())
		}
	]
	return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
		
		return redirect(url_for('index'))
	return render_template('login.html', title='Login', form=form)

