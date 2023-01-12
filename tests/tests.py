from main import app, build_report, best_lap_time_count, add_drivers_to_db, dict_from_db
from models import Driver
from peewee import *
import unittest
app=app


class TestAddingDataToDB(unittest.TestCase):
    def test_db(self):
        db = SqliteDatabase('test.db')
        db.connect()
        db.create_tables([Driver])
        add_drivers_to_db()
        self.assertEqual(Driver.select().where(Driver.name == 'Valtteri Bottas'), 'Valtteri Bottas')
        dict = dict_from_db()
        for key in dict.keys():
            Driver.get(Driver.abbr == key)
        db.close()
