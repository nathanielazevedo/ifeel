from flask import Flask, request, render_template, url_for,redirect, flash, session, jsonify, request
import os
from form import UserAddForm, LoginForm, FoodForm, SearchForm, UpdateProfileForm, UsersForm, UpdateFoodForm
from models import db, connect_db, User, Food
from sqlalchemy.exc import IntegrityError
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feel'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


# debug = DebugToolbarExtension(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
db.create_all()


@app.route("/")
def homepage():
    """Show homepage."""
    form = FoodForm()
    foods = (Food
            .query
            .filter(Food.feeling == 'Null')
            .all())

    formslist = []
    count = 0
    for food in foods:
        
        
        formslist.append(UpdateFoodForm(obj=food))


    return render_template('home-anon.html', form=form, foods=foods, formslist = formslist)
    

# @app.route('/users')
# def user_show(user_id):
#     """Show user profile."""

#     user = 2
    
#     foods = (Food
#                 .query
#                 .filter(Food.feeling == ' ')
#                 .all())
    
#     return render_template('users/show.html', user=user, messages=messages)



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
        user = 5
        amount = form.amount.data
        new_food = Food(food_name=food_name, user_id=user, amount=amount)
        db.session.add(new_food)
        db.session.commit()
        return redirect('/')

    else:
        return redirect('/')


@app.route('/foods/<food_id>/update', methods=['POST', 'GET'])
def update_info(food_id):
    food = Food.query.get(food_id)
    form = UpdateFoodForm(obj=food)
    


    if form.validate_on_submit():
        
        food.food_name = form.food_name.data
        food.amount = form.amount.data
        food.feeling = form.feeling.data
        
        db.session.add(food)
        db.session.commit()
        return redirect('/')

    else:
        return render_template('update.html', form = form, food = food)




@app.route('/profile', methods=['GET', 'POST'])
def display_profile():

    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    currUser = 5
    user = User.query.get(currUser)
    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        
            

        user.username = form.username.data
        user.email = form.email.data
        

        db.session.add(user)
        db.session.commit()
        return redirect('/')

    return render_template('/users/profile.html', user=user, form=form)


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

        return render_template('search.html', foods = foods, form=form)

    else:

        return render_template('search.html', form=form)



@app.route('/graph', methods=['GET'])
def graph():

    graph = requests.get("https://quickchart.io/chart?c={type:'bar',data:{labels:[2012,2013,2014,2015,2016],datasets:[{label:'Users',data:[120,60,50,180,120]}]}}")
    

    return render_template('graph.html', graph=graph)



@app.route('/users', methods=['GET', 'POST'])
def users():
    form = UsersForm()
    

    if form.validate_on_submit():
        username = form.user_name.data
        user = User.query.filter(User.username == username).all()

        return render_template('users.html', user = user, form=form)

    else:

        return render_template('users.html', form=form)


@app.route('/foods/<int:food_id>/delete', methods=["POST"])
def food_destroy(food_id):
    """Delete a message."""

    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")

    food = Food.query.get_or_404(food_id)
    # if msg.user_id != g.user.id:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")
    db.session.delete(food)
    db.session.commit()

    return redirect(f"/")





