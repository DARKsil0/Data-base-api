from peewee import *

db = SqliteDatabase('drivers.db')


class Driver(Model):
    name = CharField()
    best_lap_time = CharField()
    team = CharField()
    abbr = CharField()

    class Meta:
        database = db