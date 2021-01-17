from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, RadioField, TextAreaField, BooleanField, SelectMultipleField, widgets, SubmitField
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

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class FoodForm(FlaskForm):
    food_name = StringField('What did you eat?', validators = [InputRequired()])
    amount = SelectField('How much did you eat?', choices=[('1', 'a little'), ('2', 'some'), ('3', 'a lot')], validators = [InputRequired()])
    feeling = SelectField('choose one', choices=[('1', 'bad'), ('2', 'okay'), ('3', 'great')], validators = [InputRequired()])
    symptoms = MultiCheckboxField('Symptom', coerce=int)


class TryItForm(FlaskForm):
    food_name = StringField('What did you eat?', validators = [InputRequired()])



class SearchForm(FlaskForm):
    food_name = StringField('Search for a food', validators=[InputRequired()])
    

class UpdateProfileForm(FlaskForm):
    """UpdateForm form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    bio = TextAreaField('(Optional) Tell us about yourself')
    conditions = MultiCheckboxField('Condition', coerce=int)
    

class SearchAddForm(FlaskForm):
    search_food_name = StringField('Search from your foods.', validators=[InputRequired()])



class UpdateFoodForm(FlaskForm):
    food_name = StringField('What did you eat?', validators = [InputRequired()])
    amount = SelectField('How much did you eat?', choices=[('1', 'a little'), ('2', 'some'), ('3', 'a lot')])
    feeling = SelectField('choose one', choices=[('1', 'bad'), ('2', 'okay'), ('3', 'great')])
    symptoms = MultiCheckboxField('Symptom', coerce=int)


class SearchForm(FlaskForm):
    food_name_condition = StringField('Search for food data', validators=[InputRequired()])
    search_by = SelectField('Search By', coerce=int)
    
    
class InitialConditionsForm(FlaskForm):
    """Add conditions when user signs up"""

    conditions = MultiCheckboxField('Condition', coerce=int)


    




