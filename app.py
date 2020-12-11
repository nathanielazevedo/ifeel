from flask import Flask, request, render_template, url_for,redirect, flash, session, jsonify, request, g, abort, json
import os
import json
from form import UserAddForm, LoginForm, FoodForm, SearchForm, UpdateProfileForm, UserSearchForm, UpdateFoodForm, ExampleForm, SelectMany, SearchAddForm, AddSearchForm, SearchSpoonacular, AddSpoonacular, InitialConditionsForm
from models import db, connect_db, User, Food, Condition, UserConditions, Symptom, FoodSymptoms, FoodList, FoodConditions
from sqlalchemy.exc import IntegrityError
import requests
import pdb
from flask_debugtoolbar import DebugToolbarExtension
from functions import cleanNutrition, symptoms




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







#############################################






@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get_or_404(session[CURR_USER_KEY])

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
    """Show """

    if g.user:
        
        return redirect('/home')

    else:
        return redirect('/signup')





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
            

        except IntegrityError:
            flash("Username and/or email already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/signup/conditions")

    else:
        return render_template('signup.html', form=form)



@app.route('/signup/conditions', methods=["GET", "POST"])
def signupconditions():

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

        for each in conditions:
            condition = Condition.query.get_or_404(each)
            user.conditions.append(condition)

        db.session.add(user)
        db.session.commit()

        return redirect('/home')

    return render_template('/user/conditions.html', user=user, form=form)

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
            flash(f"Welcome back, {user.username}!", "success")
            return redirect("/")


        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)







@app.route('/logout')
def logout():
    """Handle logout of user."""

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







@app.route("/home")
def homepage():
    """Show homepage."""

    if not g.user:
        flash("Login or signup", "danger")
        return redirect("/")
    

    form = FoodForm()
    symptoms = [(c.id, c.symptom_name) for c in Symptom.query.all()]
    form.symptoms.choices = symptoms

    
    return render_template('home.html', form=form)





#Food Routes


@app.route('/food/add', methods=['POST'])
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
        food_data = form.food_name.data
        food_data2 = food_data.replace("null", "55")
        food_data3 = eval(food_data2)
        name, image, input_food_id = food_data3['name'], food_data3['image'], food_data3['id']

        # Getting the rest of the info
        user = g.user.id
        amount = form.amount.data
        feeling = form.feeling.data
        
        try:
            # Does this food already exist in our database?
            existing_food = FoodList.query.filter(FoodList.spoonacular_id == input_food_id).one()

        except:
            # If no, add it to the database.
            existing_food = FoodList(food_name=name, spoonacular_id=input_food_id, spoonacular_image= image)
            db.session.add(new_food_list)
            db.session.commit()

        new_food = Food(food_id=existing_food.id, user_id=user, amount=amount, feeling=feeling)
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

    
    return redirect('/home')




@app.route('/food/<food_id>/update', methods=['POST', 'GET'])
def update_info(food_id):
    #Update a food 


    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    food = Food.query.get_or_404(food_id)
    form = UpdateFoodForm(obj=food)
    symptomslist = []
    for each in food.symptoms:
        symptomslist.append(each.symptom_name)
        
    # form = ExampleForm()
    symptoms = [(c.id, c.symptom_name) for c in Symptom.query.all()]
    form.symptoms.choices = symptoms

    if form.validate_on_submit():
        
        food_name = form.food_name.data
        food_list_spot = FoodList.query.filter(FoodList.food_name == food_name).all()
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
        return redirect('/home')

    else:
        return render_template('/food/food-update.html', form=form, food=food, symptomslist=symptomslist)



@app.route('/userfoods', methods=['GET', 'POST'])
def user():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")


    form = SearchAddForm()
    foods = (Food
            .query
            .filter(Food.user_id == g.user.id, Food.feeling != 'Null')
            .all())

    if form.validate_on_submit():
        food = form.search_food_name.data
        foodlistspot = FoodList.query.filter(FoodList.food_name == food).all()
        try:
            food_id = foodlistspot[0].id
        except:
            flash("You haven't inputed that food")
            return render_template('/food/userfoods.html', foods=foods, form=form)
        foods = (Food.query.filter(Food.user_id == g.user.id, Food.food_id == food_id).all())
        
        # return render_template('/user/user.html', foods=foods, form=form)

    return render_template('/food/userfoods.html', foods=foods, form=form)



@app.route('/food/<int:food_id>/delete', methods=["POST"])
def food_destroy(food_id):
    """Delete a food."""

    if not g.user:
        flash("Sign up or login.", "danger")
        return redirect("/")

    food = Food.query.get_or_404(food_id)

    db.session.delete(food)
    db.session.commit()

    return redirect("/userfoods")








#########################################






#User Routes



@app.route('/user/profile', methods=['GET', 'POST'])
def display_profile():

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    
    user = User.query.get_or_404(g.user.id)


    # Making a list of all conditions the user currently has inorder to check them in the form.
    conditionslist = []
    for each in user.conditions:
        conditionslist.append(each.condition_name)

    form = UpdateProfileForm()
    
    conditions = [(c.id, c.condition_name) for c in Condition.query.all()]
    form.conditions.choices = conditions

    

    if form.validate_on_submit():
        
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.image_url = form.image_url.data
        conditions = form.conditions.data
        user.conditions.clear()
        for each in conditions:
            condition = Condition.query.get_or_404(each)
            user.conditions.append(condition)
        db.session.add(user)
        db.session.commit()
        return redirect('/home')

    return render_template('/user/profile.html', user=user, form=form, conditionslist=conditionslist)





@app.route('/user/profile/edit', methods=['GET', 'POST'])
def display_edit_profile():

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
        user.image_url = form.image_url.data
        conditions = form.conditions.data
        user.conditions.clear()

        for each in conditions:
            condition = Condition.query.get_or_404(each)
            user.conditions.append(condition)

        db.session.add(user)
        db.session.commit()
        return redirect('/home')

    return render_template('/user/edit-profile.html', user=user, form=form, conditionslist=conditionslist)








    







###########################################################








#Searching Routes

@app.route('/food/search', methods=['GET', 'POST'])
def search():
    #Search for a food by name. Return all matches


    form = SearchForm()
    allfoods = FoodList.query.all()

    if form.validate_on_submit():
        foodname = form.food_name.data
        food_list_spot = FoodList.query.filter(FoodList.food_name == foodname).all()
        try:
            food = food_list_spot[0]
        except:
            flash('Nobody has eaten that yet, maybe you should')
            return render_template('/search/search-food.html', form=form, allfoods=allfoods)

        return render_template('/search/search-food.html', food = food, form=form)

    else:
        
        return render_template('/search/search-food.html', form=form, allfoods=allfoods)







@app.route('/foodbycondition/search', methods=['GET', 'POST'])
def usersearch():
    # Search for a user by name or condition


    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    form = UserSearchForm()
    conditions = [(c.id, c.condition_name) for c in Condition.query.all()]
    form.search_by.choices = conditions

    if form.validate_on_submit():
        try:
            foodname = form.food_name_condiiton.data
        except:
            flash("There is no data on that food")
            return render_template('/search/foodbycondition.html', form=form)
        search_by = form.search_by.data
        tablefood = FoodList.query.filter(FoodList.food_name == foodname).one()
        

        tablecondition = Condition.query.filter(Condition.id == search_by).one()

        foods = Food.query.filter(Food.food_id == tablefood.id).all()

        newfoods = []
        for each in foods:
            conditions = each.conditions
            for each2 in conditions:
                if each2.id == tablecondition.id:
                        newfoods.append(each)
        
        averagelist = []
        for each in newfoods:
            if each.feeling != 'Null':
                averagelist.append(int(each.feeling))
        
        average = round(sum(averagelist) / len(averagelist), 1)
        
        foodsymptomslists = []


        for each in foods:
            foodsymptomslists.append(each.symptoms)

        foodsymptoms = []




        for each in foodsymptomslists:
            for each2 in each:
                foodsymptoms.append(each2)

        symptomslists = []
        strfoodsymptoms = []
        for each in foodsymptoms:
            strfoodsymptoms.append(str(each))
        count = 0
        
        for each in symptoms:
            
            symptomslists.append(strfoodsymptoms.count(each))

        graph2 = requests.get(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{symptoms},datasets:[{{label:'Number of reports per symptom after eating {foodname}',data:{symptomslists}}}]}}}}")

        return render_template('/search/foodbycondition.html', form=form, tablefood=tablefood, average=average, graph2=graph2)

    else:
        return render_template('/search/foodbycondition.html', form=form)






    

##############################################









#Graph API route

@app.route('/graph/<food_id>', methods=['GET'])
def graph(food_id):
    #Route for generating graphs. 


    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    alldata = Food.query.filter(Food.food_id == food_id).all()
    try:
        foodname = alldata[0].food_name
    except:

        form = SearchForm()
        allfoods = FoodList.query.all()


        flash("Sorry, we don't have any data on that food yet")
        return render_template('/search/search-food.html', form=form, allfoods=allfoods)

    fooddata = []
    foodsymptomslists = []

    for each in alldata:
        fooddata.append(each.feeling)
        foodsymptomslists.append(each.symptoms)



    # symptoms = Symptom.query.all()

    
    # for each in symptoms:
    #     symptomslist.append(foodsymptoms.count(each))
    length = len(fooddata)
    bads = fooddata.count('1') 
    goods = fooddata.count('2') 
    greats = fooddata.count('3') 
    fooddata.clear()
    fooddata.append(bads)
    fooddata.append(goods)
    fooddata.append(greats)



    foodsymptoms = []




    for each in foodsymptomslists:
        for each2 in each:
            foodsymptoms.append(each2)

    symptomslists = []
    strfoodsymptoms = []
    for each in foodsymptoms:
        strfoodsymptoms.append(str(each))
    count = 0
    
    for each in symptoms:
        
        symptomslists.append(strfoodsymptoms.count(each))

            
    
    graph = requests.get(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:['Bad','Good','Great'],datasets:[{{label:'Number of reports per feeling (1-3) after eating {foodname}',data:{fooddata}}}]}}}}")


    graph2 = requests.get(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{symptoms},datasets:[{{label:'Number of reports per symptom after eating {foodname}',data:{symptomslists}}}]}}}}")

    
    nutritional_info = requests.get(f"https://api.spoonacular.com/food/ingredients/{alldata[0].info.spoonacular_id}/information?amount=1&apiKey=b7e7c1efd70843b7a897ec8eb3717e34&unit=serving").json()

    nutrition = cleanNutrition(nutritional_info)
    return render_template('food/graph.html', graph=graph, graph2=graph2, foodname=foodname, nutrition=nutrition)









@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    
    return render_template('404.html'), 404




@app.route('/foodlist', methods=['GET'])
def foodlist():
    foodlist = FoodList.query.all()

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    foodnamelist = []
    for each in foodlist:
        name = each.food_name
        foodnamelist.append(name)
    return jsonify(foodnamelist)







