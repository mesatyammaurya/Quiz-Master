from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField
from wtforms.validators import Email, Length, EqualTo, DataRequired  



'''=========================================== Register Form ============================================================='''
class userRegistrationForm(FlaskForm):
    email = StringField("Username(Email):", validators=[Email()])
    name = StringField(" Full Name:", validators=[DataRequired()])
    password = PasswordField("Password:", validators=[Length(min=8)])
    confirm_password =  PasswordField("Confirm Password:", validators=[EqualTo("password")])
    qualification = StringField("Qualification:", validators=[DataRequired()])
    dob = DateField("Date of Birth:", format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField("submit")

'''=========================================== Login Form ============================================================='''
class loginForm(FlaskForm):
    email = StringField("Username(Email):", validators=[Email()])
    password = PasswordField("Password:", validators=[Length(min=8)])
    submit = SubmitField("submit")