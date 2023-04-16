from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	remember_me = BooleanField(_l('Remember Me'))
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField(_l('Username'), validators=[DataRequired()])
	email = StringField(_l("Email"), validators=[Email(), DataRequired()])
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	repeat_password = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l('Register'))
	
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError(_l("Username already in use! Please choose another."))
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError(_l("Email address already in use! Please choose another."))


class ResetPasswordRequestForm(FlaskForm):
	email = StringField(_l('Email'), validators=[DataRequired(), Email()])
	submit = SubmitField(_l('Reset Password'))


class ResetPasswordForm(FlaskForm):
	password = PasswordField(_l('Password'), validators=[DataRequired()])
	repeat_password = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField(_l("Reset Password"))
