from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, RadioField
from wtforms.validators import InputRequired, DataRequired, Email, Length

class UserAddForm(FlaskForm):
    """Form for adding users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])

    
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])



class FoodForm(FlaskForm):
    food_name = StringField('What did you eat?', validators = [InputRequired()])
    amount = SelectField('How much did you eat?', choices=[('1', 'a little'), ('2', 'some'), ('3', 'a lot')])
    # feeling = RadioField('choose one', choices=[('1', ''), ('2', ''), ('3', '')])


class SearchForm(FlaskForm):
    food_name = StringField('Search for a food?', validators=[InputRequired()])
    

class UpdateProfileForm(FlaskForm):
    """UpdateForm form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])


class UserSearchForm(FlaskForm):
    user_name = StringField('Search for a user?', validators=[InputRequired()])
    


class UpdateFoodForm(FlaskForm):
    food_name = StringField('What did you eat?', validators = [InputRequired()])
    amount = SelectField('How much did you eat?', choices=[('1', 'a little'), ('2', 'some'), ('3', 'a lot')])
    feeling = RadioField('choose one', choices=[('1', 'bad'), ('2', 'okay'), ('3', 'great')])


class UserSearchForm(FlaskForm):
    search_by = SelectField('Search By', choices=[('username', 'username'), ('disease', 'disease')])
    username = StringField('Search for a user by name or disease', validators=[InputRequired()])
    


    