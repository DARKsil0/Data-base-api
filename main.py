from peewee import *
import report_func.report_func as report_func
from flask import Flask, render_template, request, Response
from flask_restful import Resource, Api
from flasgger import Swagger, swag_from
import xml.dom.minidom
from dicttoxml import dicttoxml
from models import Driver

db = SqliteDatabase('drivers.db')


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


def dict_from_db():
    driver_dict = {}
    for driver in Driver.select():

        key = driver.abbr
        value = {'name': driver.name, 'abbr': driver.abbr, 'team':driver.team, 'best lap time': driver.best_lap_time}
        driver_dict[key] = value
    return driver_dict


db.close()


app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)


class DriversReport(Resource):

    def get(self, version):
        format = request.args.get('format')
        racer_dict = dict_from_db()

        if format == 'json':
            return racer_dict

        elif format == 'xml':
            report_xml = dicttoxml(racer_dict)
            return Response(report_xml, mimetype='application/xml')


api.add_resource(DriversReport, '/api/<version>/report/')


if __name__ == '__main__':
    #add_drivers_to_db()
    app.run(debug=True)