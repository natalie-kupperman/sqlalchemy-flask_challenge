# FLASK API SCRIPT

##############################################

# import dependencies
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

###############################################

# connect database
engine = create_engine("sqlite:///hawaii.sqlite")
inspector = inspect(engine)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine=engine, reflect=True)    

# save references to variables
station = Base.classes.station_info
measurements = Base.classes.climate_measurements

# create session from python to the database
session = Session(bind=engine)

###############################################

# flask set-up
app = Flask(__name__)

###############################################

# flask routes

@app.route("/")
def welcome():
    print("Server received request for 'Home' page...")
    
    """List all available api routes"""
    
    return ("Welcome to the Hawaii Surfer's Analysis API<br/><br/>"
            
        f"Avalable Endpoints:<br/>"
            
        f"/api/v1.0/precipitation - precipation data (in inches)<br/>"

        f"/api/v1.0/stations - information on weather collection stations <br/>"

        f"/api/v1.0/temperature - temperature observations (tobs) <br/>"

       f"/api/v1.0/*enter start date in Y-m-d format*<br/>"
            
       f"/api/v1.0/*enter start date in Y-m-d format*/*enter end date in Y-m-d format*<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    
    """Query for the dates and precip observations from the last year"""
    
    print("Server received request for precipitation page...")
    
    prcp = pd.DataFrame(session.query(measurements.date, measurements.prcp).\
           filter(measurements.date.between('2016-08-23', '2017-08-23')).all())
                        
    prcp = prcp.set_index('date')
                        
    prcp = prcp.to_dict()

    return jsonify(prcp)
                        
@app.route("/api.v1.0/stations")
def stations():
    
    """Query station names"""
    
    print("Server received request for station page...")
    
    station = pd.DataFrame(session.query(stations.name))
    
    return jsonify(station)

@app.route("/api.v1.0/temperature")
def temp():
    
    """Query temperature oberservations from the last year"""
    
    print("server received request for tobs page...")
    
    tobs = pd.DataFrame(session.query(measurements.date, measurements.tobs).\
           filter(measurements.data.between('2016-08-23', '2017-08-23')).all())
    
    return jsonify(tobs)

@app.route("/api.v1.0/<start>")
def temp_input(start):
    
    def start_temp(start_date):
        
        print("Server received request for start page...")
        data = pd.DataFrame(session.query(measurement.tobs).\
        filter(measurement.date >= start_date).all())

        avg = round(data['tobs'].mean())
        low = data['tobs'].min()
        high = data['tobs'].max()
        return avg, low, high

    average, minimum, maximum = start_temp(start)
    dictionary = {"Minimum_Temp": str(minimum), "Average_Temp": str(average), "Max_Temp": str(maximum)}
    return jsonify(dictionary)

# Return a json list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>/<end>")
# create first function to gather inputs from user in address line then pushes them into nested dunction
def temp_input_end(start, end):
    
    def calc_temps(start_date, end_date):
        print("Server received request for start/end page...")
        data = pd.DataFrame(session.query(measurement.tobs).\
        filter(measurement.date >= start_date, measurement.date < end_date).all())

        avg = round(data['tobs'].mean())
        low = data['tobs'].min()
        high = data['tobs'].max()
        return avg, low, high

    average,minimum,maximum = calc_temps(start, end)
    dictionary = {"Minimum_Temp" : str(minimum), "Average_Temp" : str(average), "Max_Temp" : str(maximum)}
    
    return jsonify(dictionary)

if __name__ == '__main__':
    app.run()

