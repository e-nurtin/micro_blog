from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField("Email", validators=[Email(), DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	repeat_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')
	
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError("Username already in use! Please choose another.")
	
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError("Email address already in use! Please choose another.")


class EditProfileForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
	submit = SubmitField('Submit')
	
	def __init__(self, original_username, *args, **kwargs):
		super(EditProfileForm, self).__init__(*args, **kwargs)
		self.original_username = original_username
	
	def validate_username(self, username):
		if username.data != self.original_username:
			user = User.query.filter_by(username=self.username.data).first()
			
			if user is not None:
				raise ValidationError("The username already in use! Please choose a different username.")
		
		
class EmptyForm(FlaskForm):
	submit = SubmitField('Submit')
	
	
class PostForm(FlaskForm):
	post = TextAreaField("Say what's on your mind", validators=[
		DataRequired(), Length(min=1, max=140)])
	submit = SubmitField('Submit')
	
	
class ResetPasswordRequestForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Reset Password')
	
	
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	repeat_password = PasswordField('Reapeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Reset Password")