from flask import Flask, request, render_template, url_for,redirect, flash, session, jsonify, request
import os
from form import UserAddForm, LoginForm, FoodForm, SearchForm
from models import db, connect_db, User, Food
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

\
# debug = DebugToolbarExtension(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Show homepage."""
    form = FoodForm()
    foods = Food.query.all()
    return render_template('home-anon.html', form=form, foods = foods)




@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()
            user = username=form.username.data

        except IntegrityError:
            flash("Username and/or email already taken", 'danger')
            return render_template('signup.html', form=form)

        # do_login(user)

        return redirect("/")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)



@app.route('/add', methods=['POST'])

def post_info():

    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    form = FoodForm()

    if form.validate_on_submit():
        food_name = form.food_name.data
        user = 1
        amount = form.amount.data
        new_food = Food(food_name=food_name, user_id=user, amount=amount)
        db.session.add(new_food)
        db.session.commit()
        return redirect('/')

    else:
        return redirect('/')




@app.route('/profile', methods=['GET'])


def display_profile():

    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    currUser = 1
    user = User.query.get(currUser)

    return render_template('/users/profile.html', user=user)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = SearchForm()
    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    # currUser = 1
    # user = User.query.get(currUser)



    if form.validate_on_submit():
        foodname = form.food_name.data
        foods = Food.query.filter(Food.food_name == foodname).all()

        return render_template('search.html', foods = foods, form = form)

    else:

        return render_template('search.html', form=form)