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


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"



    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

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

    user = db.relationship('User', backref='posts',  cascade="all,delete")