from peewee import *
import report_func.report_func as report_func


db = SqliteDatabase('drivers.db')


class Driver(Model):
    name = CharField()
    best_lap_time = CharField()
    team = CharField()
    abbr = CharField()

    class Meta:
        database = db


def build_report():
    dict_abbr_class = report_func.make_classes('logs')
    dict_abbr_class = report_func.add_time_to_class('logs', 'start', dict_abbr_class)
    dict_abbr_class = report_func.add_time_to_class('logs', 'end', dict_abbr_class)
    return dict_abbr_class


def best_lap_time_count(value):
    if value.lap_time is not None:
        best_lap_time = str(value.lap_time)
    else:
        best_lap_time = 'Invalid data about lap time.'
    return best_lap_time


db.connect()

db.create_tables([Driver])


def add_drivers_to_db():
    dict_abbr_class = build_report()
    for abbr, value in dict_abbr_class.items():
        abbr = Driver.create(name=value.name, team=value.team, best_lap_time=best_lap_time_count(value), abbr=abbr)


db.close()


if __name__ == '__main__':
    add_drivers_to_db()