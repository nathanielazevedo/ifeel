from flask import Flask, request, render_template, url_for,redirect, flash, session, jsonify, request, g, abort
import os
from form import UserAddForm, LoginForm, FoodForm, SearchForm, UpdateProfileForm, UserSearchForm, UpdateFoodForm
from models import db, connect_db, User, Food
from sqlalchemy.exc import IntegrityError
import requests


CURR_USER_KEY = "curr_user"

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









#############################################




@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



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
    """Show homepage:

    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        
        return redirect('/homepage')

    else:
        return redirect('/signup')




@app.route("/homepage")
def homepage():
    """Show homepage."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")


    form = FoodForm()
    foods = (Food
            .query
            .filter(Food.feeling == 'Null')
            .all())

    return render_template('homepage.html', form=form, foods=foods)
    






##########################################







#Sigup Route


@app.route('/signup', methods=["GET", "POST"])
def signup():
    #Sign a user up.

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()
            # user = username=form.username.data

        except IntegrityError:
            flash("Username and/or email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/homepage")

    else:
        return render_template('signup.html', form=form)




#Login Route


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



@app.route('/logout')
def logout():
    """Handle logout of user."""
    # print(f'Heres the session info{session[curr_user]}')
    # IMPLEMENT THIS


    do_logout()
    flash("You've been signed out", 'success')
    return redirect("/login")



@app.route('/users/delete', methods=["POST"])
def delete_user():
    """Delete user."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    return redirect("/signup")








######################################













#Food Routes


@app.route('/food/add', methods=['POST'])
def post_info():

    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = FoodForm()

    if form.validate_on_submit():
        food_name = form.food_name.data
        user = g.user.id
        amount = form.amount.data
        new_food = Food(food_name=food_name, user_id=user, amount=amount)
        db.session.add(new_food)
        db.session.commit()
        return redirect('/homepage')

    else:
        return redirect('/homepage')






@app.route('/food/<food_id>/update', methods=['POST', 'GET'])
def update_info(food_id):
    #Update a food 


    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    food = Food.query.get(food_id)
    form = UpdateFoodForm(obj=food)

    if form.validate_on_submit():
        
        food.food_name = form.food_name.data
        food.amount = form.amount.data
        food.feeling = form.feeling.data
        
        db.session.add(food)
        db.session.commit()
        return redirect('/homepage')

    else:
        return render_template('/food/food-update.html', form=form, food=food)






@app.route('/food/<int:food_id>/delete', methods=["POST"])
def food_destroy(food_id):
    """Delete a food."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    food = Food.query.get_or_404(food_id)

    db.session.delete(food)
    db.session.commit()

    return redirect("/homepage")











#########################################










#User Routes


@app.route('/user/profile', methods=['GET', 'POST'])
def display_profile():

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    currUser = g.user.id
    user = User.query.get(currUser)
    form = UpdateProfileForm(obj=user)

    if form.validate_on_submit():
        
        user.username = form.username.data
        user.email = form.email.data
        
        db.session.add(user)
        db.session.commit()
        return redirect('/homepage')

    return render_template('/user/profile.html', user=user, form=form)





@app.route('/user/<user_id>', methods=['GET', 'POST'])
def display_specific_profile(user_id):

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    
    user = User.query.get(user_id)

    return render_template('/user/user-profile.html', user=user)  





@app.route('/user', methods=['GET'])
def user():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    foods = (Food
            .query
            .filter(Food.user_id == g.user.id, Food.feeling != 'Null')
            .all())

    return render_template('/user/user.html', foods=foods)
    












###########################################################











#Searching Routes

@app.route('/food/search', methods=['GET', 'POST'])
def search():
    #Search for a food by name. Return all matches


    form = SearchForm()
    # if not g.user:
    #     flash('Please login first!')
    #     return redirect('/login')


    if form.validate_on_submit():
        foodname = form.food_name.data
        foods = Food.query.filter(Food.food_name == foodname).all()

        return render_template('/search/search-food.html', foods = foods, form=form)

    else:

        return render_template('/search/search-food.html', form=form)





@app.route('/user/search', methods=['GET', 'POST'])
def usersearch():
    # Search for a user by name or condition


    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    form = UserSearchForm()

    if form.validate_on_submit():
        username = form.username.data
        search_by = form.search_by.data
        
        if search_by == 'username':
            users = User.query.filter(User.username == username).all()
        
        else:
            users = User.query.filter(User.username == usernamename).all()

        return render_template('/search/search-users.html', users = users, form=form)

    else:
        return render_template('/search/search-users.html', form=form)










##############################################









#Graph API route

@app.route('/graph', methods=['GET'])
def graph():
    #Route for generating graphs. Needs developing

    graph = requests.get("https://quickchart.io/chart?c={type:'bar',data:{labels:[2012,2013,2014,2015,2016],datasets:[{label:'Users',data:[120,60,50,180,120]}]}}")
    
    return render_template('graph.html', graph=graph)













