from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import datetime
from datetime import datetime, timedelta, date



db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/feellogo.png",
    )

    bio = db.Column(
        db.Text,
    )



    foods = db.relationship('Food', cascade='all, delete')

    conditions = db.relationship('Condition',
                               secondary='users_conditions',
                               backref='users')


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"



    @classmethod
    def signup(cls, username, email, password):
        """Sign up user."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`."""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Food(db.Model):
    from datetime import date, datetime
    import datetime
    

    __tablename__ = "foods"

    id = db.Column(db.Integer, 
                primary_key=True, 
                autoincrement=True)

    food_name = db.Column(db.Text, 
                        nullable=False, 
                        unique=False)

    amount = db.Column(db.Text, nullable=True)

    feeling = db.Column(db.Text, nullable = True, default = 'Null')

    timestamp = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.utcnow(),
    )

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User')

    symptoms = db.relationship('Symptom',
                               secondary='foods_symptoms',
                               backref='foods')



class UserConditions(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'users_conditions'

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        primary_key=True,
    )

    condition_id = db.Column(
        db.Integer,
        db.ForeignKey('conditions.id', ondelete="cascade"),
        primary_key=True,
    )



class Condition(db.Model):


    __tablename__ = 'conditions'

    id = db.Column(db.Integer, 
                primary_key=True, 
                autoincrement=True)

    condition_name = db.Column(db.Text)


    # user = db.relationship('User',
    #                            secondary='users_conditions',
    #                            backref='conditions')





class FoodSymptoms(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'foods_symptoms'

    food_id = db.Column(
        db.Integer,
        db.ForeignKey('foods.id', ondelete="cascade"),
        primary_key=True,
    )

    symptom_id = db.Column(
        db.Integer,
        db.ForeignKey('symptoms.id', ondelete="cascade"),
        primary_key=True,
    )


class Symptom(db.Model):


    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, 
                primary_key=True, 
                autoincrement=True)

    symptom_name = db.Column(db.Text)