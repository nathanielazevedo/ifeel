from flask import Flask, request, render_template, url_for, redirect, flash, session, jsonify, request, g, abort, json
from functions import makeGraph, makeEmptyGraph, genFoodGraph, makeBarGraph, symptoms, analyzeUserFoods, populateSearchConditions, analyzeFoodData, analyzeFoodDataCondition
from form import UserAddForm, LoginForm, FoodForm, SearchForm, UpdateProfileForm, SearchForm, UpdateFoodForm,   SearchAddForm, InitialConditionsForm, TryItForm
from models import db, connect_db, User, Food, Condition, UserConditions, Symptom, FoodSymptoms, FoodList, FoodConditions
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
import os
import json
import requests
import pdb



app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///feel')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
debug = DebugToolbarExtension(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
db.create_all()

CURR_USER_KEY = "curr_user"

#####################################################

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])

    else:
        g.user = None


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


#####################################################


@app.route('/')
def main():
    """Show homepage or signup page depending on global user variable"""

    if g.user:
        return redirect('/home')

    else:
        return redirect('/signup')


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user by delete user info from session"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Sign a user in or take them to signup page"""

    form = UserAddForm()
    form2 = TryItForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username and/or email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/signup/conditions")

    else:
        return render_template('signup.html', form=form, form2=form2)


@app.route('/signup/conditions', methods=["GET", "POST"])
def signupconditions():
    """Allow user to add conditions after signup"""

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    user = User.query.get_or_404(g.user.id)

    # Making a list of all conditions the user currently has inorder to check them in the form.

    form = InitialConditionsForm()

    # Populating conditions options for form.
    conditions = [(c.id, c.condition_name) for c in Condition.query.all()]
    form.conditions.choices = conditions

    if form.validate_on_submit():

        conditions = form.conditions.data

        # Add each submitted condition to the user_conditions table
        for each in conditions:
            condition = Condition.query.get_or_404(each)
            user.conditions.append(condition)

        db.session.add(user)
        db.session.commit()

        return redirect('/home')

    return render_template('/user/conditions.html', user=user, form=form)


@app.route('/generic', methods=["GET"])
def generic():
    """Signup as generic user, for users that want to see app but not signup"""

    user = User.authenticate('test', 'password')

    do_login(user)
    return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    """Login a user or take them to login page"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Log a user out"""

    do_logout()
    flash("You've been signed out", 'success')
    return redirect("/login")


@app.route('/users/delete')
def delete_user():
    """Delete a users profile"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")


@app.route("/home")
def homepage():
    """Show homepage. Generate day, week, month graphs from user foods"""

    if not g.user:
        flash("Login or signup", "danger")
        return redirect("/")

    foods = (Food.query.filter(Food.user_id == g.user.id).all())

    total = len(foods)

    # If user has no foods inputed, show generic graphs on homepage.
    if (total == 0):
        graph = makeEmptyGraph()
        return render_template('home.html', graph2=graph, graph=graph, graph3=graph)

    # Generate user homepage graphs.
    result = analyzeUserFoods(foods)
    graph, graph2, graph3 = result

    return render_template('home.html', graph=graph, graph2=graph2, graph3=graph3)



@app.route('/food/add', methods=['POST', 'GET'])
def post_info():
    '''Add a food '''

    if not g.user:
        flash("Please login or signup.", "danger")
        return redirect("/")

    form = FoodForm()

    # Filling in form checkbox choices with database info.
    symptoms = [(c.id, c.symptom_name) for c in Symptom.query.all()]
    form.symptoms.choices = symptoms

    if form.validate_on_submit():

        # Getting food information
        food_data = json.loads(form.food_name.data)
        name, image, input_food_id = food_data['name'], food_data['image'], food_data['id']
        amount = form.amount.data
        feeling = form.feeling.data

        try:
            # Does this food already exist in our database?
            existing_food = FoodList.checkFor(input_food_id)
            
        except:
            # If no, add it to the database.
            existing_food = FoodList(food_name = name, spoonacular_id = input_food_id, spoonacular_image = image)
            db.session.add(existing_food)
            db.session.commit()

        new_food = Food(food_id = existing_food.id, user_id = g.user.id, amount = amount, feeling = feeling)
        db.session.add(new_food)
        db.session.commit()

        # Appending symptoms to this consumption instance.
        symptoms = form.symptoms.data

        for each in symptoms:
            symptom = Symptom.query.get_or_404(each)
            new_food.symptoms.append(symptom)

        # Appending users conditions to this consumption instance.
        for each in g.user.conditions:
            new_food.conditions.append(each)

        db.session.commit()
        flash(f'{name} has been added to your foods.')
        return redirect('/userfoods')

    return render_template('/food/addfood.html', form=form)


@app.route('/food/<food_id>/update', methods=['POST', 'GET'])
def update_info(food_id):
    """Update a food consumption instance"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    food = Food.query.get_or_404(food_id)
    form = UpdateFoodForm(obj=food)
    symptomslist = []
    for each in food.symptoms:
        symptomslist.append(each.symptom_name)

    symptoms = [(c.id, c.symptom_name) for c in Symptom.query.all()]
    form.symptoms.choices = symptoms

    if form.validate_on_submit():

        food_name = form.food_name.data
        food_list_spot = FoodList.query.filter(
            FoodList.food_name == food_name).all()
        food.food_id = food_list_spot[0].id
        food.amount = form.amount.data
        food.feeling = form.feeling.data
        symptoms = form.symptoms.data
        food.symptoms.clear()
        for each in symptoms:
            symptom = Symptom.query.get_or_404(each)
            food.symptoms.append(symptom)

        db.session.add(food)
        db.session.commit()
        flash('That input has been updated.')
        return redirect('/userfoods')

    else:
        return render_template('/food/food-update.html', form=form, food=food, symptomslist=symptomslist)


@app.route('/userfoods', methods=['GET'])
def user():
    """Show all food inputs from a user"""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchAddForm(request.args)
    foods = (Food
             .query
             .filter(Food.user_id == g.user.id, Food.feeling != 'Null')
             .order_by(Food.timestamp.desc())
             )

    if form.search_food_name.data:
        food = form.search_food_name.data
        foodlistspot = FoodList.query.filter(FoodList.food_name == food).all()
        try:
            food_id = foodlistspot[0].id
        except:
            flash("You haven't inputed that food")
            return render_template('/food/userfoods.html', foods=foods, form=form)
        foods = (Food.query.filter(Food.user_id ==
                                   g.user.id, Food.food_id == food_id).all())

    return render_template('/food/userfoods.html', foods=foods, form=form)


@app.route('/food/<int:food_id>/delete')
def food_destroy(food_id):
    """Delete a food."""

    if not g.user:
        flash("Sign up or login.", "danger")
        return redirect("/")

    food = Food.query.get_or_404(food_id)

    db.session.delete(food)
    db.session.commit()
    flash('Successfully deleted')

    return redirect("/userfoods")


@app.route('/user/profile', methods=['GET', 'POST'])
def display_profile():
    """Display the users profile"""

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    # Making a list of all conditions the user currently has inorder to check them in the form.
    conditionslist = []
    for each in g.user.conditions:
        conditionslist.append(each.condition_name)

    form = UpdateProfileForm()

    conditions = [(c.id, c.condition_name) for c in Condition.query.all()]
    form.conditions.choices = conditions

    return render_template('/user/profile.html', user=user, form=form, conditionslist=conditionslist)


@app.route('/user/profile/edit', methods=['GET', 'POST'])
def edit_profile():

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    user = User.query.get_or_404(g.user.id)

    # Making a list of all conditions the user currently has inorder to check them in the form.
    conditionslist = []
    for each in user.conditions:
        conditionslist.append(each.condition_name)
    form = UpdateProfileForm(obj=user)

    # Populating conditions options for form.
    conditions = [(c.id, c.condition_name) for c in Condition.query.all()]
    form.conditions.choices = conditions

    if form.validate_on_submit():

        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        conditions = form.conditions.data
        user.conditions.clear()

        for each in conditions:
            condition = Condition.query.get_or_404(each)
            user.conditions.append(condition)

        db.session.add(user)
        db.session.commit()
        return redirect('/user/profile')

    return render_template('/user/edit-profile.html', user=user, form=form, conditionslist=conditionslist)


@app.route('/search', methods=['GET'])
def foodDataSearchForm():

    form = SearchForm(request.args)
    conditions = populateSearchConditions()
    form.search_by.choices = conditions

    return render_template('/search/foodbycondition.html', form=form)


@app.route('/search/results', methods=['GET'])
def foodDataSearch():

    if not g.user:
        flash('Please login first!')
        return redirect('/login')
    
    conditions = populateSearchConditions()
    
    #Populate form with params and condition info
    form = SearchForm(request.args)
    form.search_by.choices = conditions

    food_data = json.loads(form.food_name_condition.data)
    name, image, input_food_id = food_data['name'], food_data['image'], food_data['id']

    #What condition are we filtering by.
    search_by = form.search_by.data
    
    try:
        foodFromList = FoodList.query.filter(FoodList.spoonacular_id == input_food_id).one()
        foodname = foodFromList.food_name

    except:
        flash("Sorry, we don't have any data on that food yet")
        return redirect('/search')
    
    #if no condition to filter by
    if (search_by == 0):
        alldata = Food.query.filter(Food.food_id == foodFromList.id).all()
        fooddata, symptoms, symptomslists = analyzeFoodData(alldata)
        graph = genFoodGraph(fooddata)
        graph2 = makeBarGraph(symptoms, symptomslists)
        condition = "no condition"
        
        return render_template('food/graph.html', graph=graph, graph2=graph2, foodname=foodname, condition=condition)

    #if we are searching by a condition
    else:
        tablecondition = Condition.query.filter(Condition.id == search_by).one()
        
        foods = Food.query.filter(Food.food_id == foodFromList.id).all()

        fooddata, symptoms, symptomslists = analyzeFoodDataCondition(tablecondition, foods)
        
        graph = genFoodGraph(fooddata)
        graph2 = makeBarGraph(symptoms, symptomslists)
        condition = tablecondition.condition_name

        return render_template('/food/graph.html', graph=graph, graph2=graph2, condition=condition, foodname=foodname)


@app.route('/foodlist', methods=['GET'])
def foodlist():
    """API route for getting all foods we have"""
    
    foodlist = FoodList.query.all()

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    foodnamelist = []
    for each in foodlist:
        name = each.food_name
        foodnamelist.append(name)
    return jsonify(foodnamelist)


########################################### Manifest and 404


@app.route('/manifest.json')
def manifest():
    manifest_python_object = {
        "name": "Feel",
        "short_name": "feel",
        "lang": "en-US",
        "start_url": "/",
        "display": "fullscreen",
        "theme_color": "#ffffff",
        "background_color": "#ffffff",
        "icons": [
            {
                "src": "/static/images/officiallogo.png",
                "sizes": "144x144",
                "type": "png",

            }
        ]
    }
    return jsonify(manifest_python_object)


@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""

    return render_template('404.html'), 404
