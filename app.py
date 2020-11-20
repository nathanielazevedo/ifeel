from flask import Flask, request, render_template, url_for,redirect, flash, session, jsonify, request
import os
from form import UserAddForm, LoginForm, FoodForm, SearchForm, UpdateProfileForm, UserSearchForm, UpdateFoodForm
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









#############################################









@app.route("/")
def main():
    """Redirect to homepage."""

    return redirect('/homepage')




@app.route("/homepage")
def homepage():
    """Show homepage."""


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
            user = username=form.username.data

        except IntegrityError:
            flash("Username and/or email already taken", 'danger')
            return render_template('signup.html', form=form)


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


        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)












######################################













#Food Routes


@app.route('/food/add', methods=['POST'])
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
        return redirect('/homepage')

    else:
        return redirect('/homepage')






@app.route('/food/<food_id>/update', methods=['POST', 'GET'])
def update_info(food_id):
    #Update a food 

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
    """Delete a message."""

    # if not g.user:
    #     flash("Access unauthorized.", "danger")
    #     return redirect("/")

    food = Food.query.get_or_404(food_id)

    db.session.delete(food)
    db.session.commit()

    return redirect(f"/homepage")











#########################################










#User Routes


@app.route('/user/profile', methods=['GET', 'POST'])
def display_profile():

    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    currUser = 1
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

    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

    
    user = User.query.get(user_id)

    return render_template('/user/user-profile.html', user=user)  





@app.route('/user', methods=['GET'])
def user():

    foods = (Food
            .query
            .filter(Food.user_id == 1)
            .all())

    return render_template('/user/user.html', foods=foods)
    












###########################################################











#Searching Routes

@app.route('/food/search', methods=['GET', 'POST'])
def search():
    #Search for a food by name. Return all matches


    form = SearchForm()
    # if 'user_id' not in session:
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


    # if 'user_id' not in session:
    #     flash('Please login first!')
    #     return redirect('/login')

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













