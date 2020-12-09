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
    amount = SelectField('How much did you eat?', choices=[('', 'How much did you eat?'),('1', 'a little'), ('2', 'some'), ('3', 'a lot')])
    feeling = SelectField('choose one', choices=[('0', 'How do you feel?'),('1', 'bad'), ('2', 'okay'), ('3', 'great')])
    symptoms = MultiCheckboxField('Symptom', coerce=int)










class SearchForm(FlaskForm):
    food_name = StringField('Search for a food?', validators=[InputRequired()])
    



class UpdateProfileForm(FlaskForm):
    """UpdateForm form."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    bio = TextAreaField('(Optional) Tell us about yourself')
    image_url = StringField('(Optional) Image URL')
    conditions = MultiCheckboxField('Condition', coerce=int)
    

class SearchAddForm(FlaskForm):
    search_food_name = StringField('Search For a food.', validators=[InputRequired()])
    

class AddSearchForm(FlaskForm):
    add_food_name = StringField('Add a food to database.', validators = [InputRequired()])


class UserSearchForm(FlaskForm):
    user_name = StringField('Search for a user?', validators=[InputRequired()])
    


class UpdateFoodForm(FlaskForm):
    food_name = StringField('What did you eat?', validators = [InputRequired()])
    amount = SelectField('How much did you eat?', choices=[('1', 'a little'), ('2', 'some'), ('3', 'a lot')])
    feeling = SelectField('choose one', choices=[('1', 'bad'), ('2', 'okay'), ('3', 'great')])
    symptoms = MultiCheckboxField('Symptom', coerce=int)


class UserSearchForm(FlaskForm):
    food_name = StringField('Search for a food by condition', validators=[InputRequired()])
    search_by = SelectField('Search By', coerce=int)
    
    



    
class ExampleForm(FlaskForm):
    Condition = MultiCheckboxField('Condition', coerce=int)
    submit = SubmitField("Set User Choices")


class SelectMany(FlaskForm):

    Condition = SelectMultipleField("Condition", coerce=int)


class SearchSpoonacular(FlaskForm):
    spoonacular_food_name = StringField('Search For a food to add', validators=[InputRequired()])


class AddSpoonacular(FlaskForm):
    spoonacular_food_name = StringField('', validators=[InputRequired()])