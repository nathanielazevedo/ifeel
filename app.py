from flask import Flask, request, render_template, url_for,redirect, flash, session, jsonify, request, g, abort
import os
from form import UserAddForm, LoginForm, FoodForm, SearchForm, UpdateProfileForm, UserSearchForm, UpdateFoodForm, ExampleForm, SelectMany, SearchAddForm, AddSearchForm
from models import db, connect_db, User, Food, Condition, UserConditions, Symptom, FoodSymptoms, FoodList
from sqlalchemy.exc import IntegrityError
import requests


CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SECRET_KEY'] = "verysecret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///feel')
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

    amounts = ['', 'a little', 'some', 'a lot']
    form = FoodForm()
    foods = (Food
            .query
            .filter(Food.feeling == 'Null', Food.user_id == g.user.id)
            .all())

    
    return render_template('homepage.html', form=form, foods=foods, amounts=amounts)
    






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
            flash(f"Welcome back, {user.username}!", "success")
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


    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    

    form = FoodForm()

    if form.validate_on_submit():
        food_name = form.food_name.data
        food_list_spot = FoodList.query.filter(FoodList.food_name == food_name).all()
        if food_list_spot:
            food_id = food_list_spot[0].id
            user = g.user.id
            amount = form.amount.data
            new_food = Food(food_id=food_id, user_id=user, amount=amount)
            db.session.add(new_food)
            db.session.commit()
            return redirect('/homepage')
        else:
            flash('Not in database. Add it! Bottom right.')
            return redirect('/homepage')

    else:
        return redirect('/homepage')






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
        return redirect('/homepage')

    else:
        return render_template('/food/food-update.html', form=form, food=food, symptomslist=symptomslist)






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
    user = User.query.get_or_404(currUser)
    conditionslist = []
    for each in user.conditions:
        conditionslist.append(each.condition_name)
    form = UpdateProfileForm(obj=user)
    # form = ExampleForm()
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
        return redirect('/homepage')

    return render_template('/user/profile.html', user=user, form=form, conditionslist=conditionslist)







@app.route('/user/profile/edit', methods=['GET', 'POST'])
def display_edit_profile():

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    currUser = g.user.id
    user = User.query.get_or_404(currUser)
    conditionslist = []
    for each in user.conditions:
        conditionslist.append(each.condition_name)
    form = UpdateProfileForm(obj=user)
    # form = ExampleForm()
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
        return redirect('/homepage')

    return render_template('/user/edit-profile.html', user=user, form=form, conditionslist=conditionslist)





@app.route('/user/<user_id>', methods=['GET', 'POST'])
def display_specific_profile(user_id):

    if not g.user:
        flash('Please login first!')
        return redirect('/login')

    
    user = User.query.get_or_404(user_id)

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


    if form.validate_on_submit():
        foodname = form.food_name.data
        food_list_spot = FoodList.query.filter(FoodList.food_name == foodname).all()
        food = food_list_spot[0]
        paverage = Food.query.filter(Food.food_id == food_list_spot[0].id).all()
        averagelist = []
        for each in paverage:
            if each.feeling != 'Null':
                averagelist.append(int(each.feeling))
        print(f'%%%%%%%%%%%{averagelist}')
        average = sum(averagelist) / len(averagelist)

        # food_id = food_list_spot[0]
        # food = Food.query.filter(Food.food_id == food_id).first()

        return render_template('/search/search-food.html', food = food, form=form, average=average)

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
            condition = Condition.query.filter(Condition.condition_name == username).first()
            users = condition.users

        return render_template('/search/search-users.html', users=users, form=form)

    else:
        return render_template('/search/search-users.html', form=form)










##############################################







symptoms = ['acid reflux', 'diarrhea', 'constipation', 'heart burn', 'bloating', 'naseau', 'gas', 'upset stomach', 'abdominal pain', 'cramps', 'vomitting']

#Graph API route

@app.route('/graph/<food_id>', methods=['GET'])
def graph(food_id):
    #Route for generating graphs. Needs developing
    alldata = Food.query.filter(Food.food_id == food_id).all()
    foodname = alldata[0].food_name
    foodsymptomslists = []
    foodsymptoms = []
    fooddata = []
    for each in alldata:
        fooddata.append(each.feeling)
        foodsymptomslists.append(each.symptoms)


    for each in foodsymptomslists:
            for each2 in each:
                foodsymptoms.append(each2)

    # symptoms = Symptom.query.all()

    symptomslists = []
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
    strfoodsymptoms = []
    for each in foodsymptoms:
        strfoodsymptoms.append(str(each))
    count = 0
    
    for each in symptoms:
        
        symptomslists.append(strfoodsymptoms.count(each))

            
    
    graph = requests.get(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:['Bad','Good','Great'],datasets:[{{label:'Number of reports per feeling (1-3) after eating {foodname}',data:{fooddata}}}]}}}}")


    graph2 = requests.get(f"https://quickchart.io/chart?c={{type:'bar',data:{{labels:{symptoms},datasets:[{{label:'Number of reports per symptom after eating {foodname}',data:{symptomslists}}}]}}}}")
    
    return render_template('graph.html', graph=graph, graph2=graph2, foodname=foodname)






@app.route('/foodlist', methods=['GET'])
def foodlist():
    foodlist = FoodList.query.all()


    foodnamelist = []
    for each in foodlist:
        name = each.food_name
        foodnamelist.append(name)
    return jsonify(foodnamelist)





@app.errorhandler(404)
def page_not_found(e):
    """404 NOT FOUND page."""
    
    return render_template('404.html'), 404



@app.route('/food/database/add', methods=['GET','POST'])
def addtodatabase():
    """"""
    form = SearchAddForm()
    form2 = AddSearchForm()
    allfoods = FoodList.query.all()

    if form.validate_on_submit():
        foodname = form.search_food_name.data
        allfoods = FoodList.query.filter(FoodList.food_name.like(f"%{foodname}%")).all()
        return render_template('allfoods.html', allfoods=allfoods, form=form, form2=form2) 

    elif form2.validate_on_submit():
        foodname = form2.add_food_name.data
        new_food = FoodList(food_name=foodname)
        db.session.add(new_food)
        db.session.commit()
        flash(f'{foodname} added to database.')
        return redirect('/homepage')


    return render_template('allfoods.html', allfoods=allfoods, form=form, form2=form2)
