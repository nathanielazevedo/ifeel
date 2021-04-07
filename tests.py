from app import app
import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, connect_db, User, Food, Condition, UserConditions, Symptom, FoodSymptoms, FoodList, FoodConditions

os.environ['DATABASE_URL'] = "postgresql:///feel-test"


db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.uid = 94566
        u = User.signup("testing", "testing@test.com", "password")
        u.id = self.uid
        db.session.commit()

        self.u = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_food_model(self):

        food = 'chicken'
        fl = FoodList(
            food_name=food,
            spoonacular_id='1'
        )

        db.session.add(fl)
        db.session.commit()

        f = Food(
            food_id="1",
            user_id=self.uid
        )

        db.session.add(f)
        db.session.commit()

        self.assertEqual(len(self.u.foods), 1)
        self.assertEqual(self.u.foods[0].food_id, 1)

    def test_conditions_model(self):

        condition = 'ibs'

        c = Condition(
            condition_name=condition
        )

        db.session.add(c)
        db.session.commit()

        self.u.conditions.append(c)

        db.session.commit()

        self.assertEqual(len(self.u.conditions), 1)
        self.assertEqual(self.u.conditions[0].condition_name, condition)

    def test_symptoms_model(self):

        food = 'chicken'
        fl = FoodList(
            food_name=food,
            spoonacular_id='1'
        )

        db.session.add(fl)
        db.session.commit()

        f = Food(
            food_id="1",
            user_id=self.uid
        )

        db.session.add(f)
        db.session.commit()

        symptom = 'bloating'

        s = Symptom(
            symptom_name=symptom
        )

        db.session.add(s)
        db.session.commit()

        f.symptoms.append(s)

        db.session.commit()

        self.assertEqual(len(f.symptoms), 1)
        self.assertEqual(f.symptoms[0].symptom_name, symptom)
