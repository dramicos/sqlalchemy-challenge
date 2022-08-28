import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements= Base.classes.measurement
stations = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Set the most recent date in db as a global so it can be called into different routes
session = Session(engine)

most_recent_date = session.query(measurements.date).order_by('date')[-1][0]
earliest_date = session.query(measurements.date).order_by('date')[0][0]

session.close()

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/YYYY-MM-DD<br/>"
        f"/api/v1.0/YYYY-MM-DD/YYYY-MM-DD<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precip():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all dates and precipitation
    results = session.query(measurements.date,measurements.prcp).all()

    session.close()

    # Create the dictionary
    precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
                
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)


@app.route("/api/v1.0/stations")
def station_fn():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all stations
    results = session.query(stations.station).all()

    session.close()

    # Create a list from the row data and save it
    stations_list = list(np.ravel(results))


    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobserves():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # using the same method as in the climate_hawaii.ipynb to get last year data
    from dateutil.relativedelta import relativedelta
    
    query_date = dt.date.fromisoformat(most_recent_date)-relativedelta(years=1)


    # Query all stations where the station was determined in climate_hawaii.ipynb
    results = session.query(measurements.date, measurements.tobs).filter(measurements.station == 'USC00519281').\
        filter(measurements.date >= query_date.isoformat() ).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    # Create the dictionary
    tob = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
                
        tob.append(tobs_dict)


    return jsonify(tob)


@app.route("/api/v1.0/<start>")
def tobs_for_date(start):
    # Set the date value for query and ensure in correct format
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    except:
        return(f'You must enter a date in the format YYYY-MM-DD')
        
    first_date = dt.datetime.strptime(earliest_date, '%Y-%m-%d').date()
    last_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Ensure dates are in the range of the available data
    if start_date < first_date:
        return(f'The date {start_date} is before the earliest recorded date {first_date}.')
    
    elif start_date > last_date:
        return(f'The date {start_date} is later than the last recorded date {last_date}.')
           
    else:
        results = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
            filter(measurements.date >= start_date).all()
        
        tobs_dict = {}
        tobs_dict["TMIN"] = results[0][0]
        tobs_dict["TMAX"] = results[0][1]
        tobs_dict["TAVG"] = results[0][2]
        
        return jsonify(tobs_dict)
 

@app.route("/api/v1.0/<start>/<end>")
def tobs_for_dates(start, end):
    # Set the date values for query and ensure in correct format
    
    try:
        start_date = dt.datetime.strptime(start, '%Y-%m-%d').date()
    except:
        return(f'You must enter dates in the format YYYY-MM-DD')
    
    try:
        end_date = dt.datetime.strptime(end, '%Y-%m-%d').date()
    except:
        return(f'You must enter dates in the format YYYY-MM-DD')
    
    first_date = dt.datetime.strptime(earliest_date, '%Y-%m-%d').date()
    last_date = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Ensure dates are in the range of the available data and that the start is before the end
    if start_date < first_date:
        return(f'The date {start_date} is before the earliest recorded date {first_date}.')
    
    elif start_date > last_date:
        return(f'The date {start_date} is later than the last recorded date {last_date}.')
    
    elif end_date < start_date:
        return(f'The date {end_date} must come before the date {start_date} in the address.')
    
    else:
        results = session.query(func.min(measurements.tobs), func.max(measurements.tobs), func.avg(measurements.tobs)).\
            filter(measurements.date >= start_date).filter(measurements.date <= end_date).all()
        
        tobs_dict = {}
        tobs_dict["TMIN"] = results[0][0]
        tobs_dict["TMAX"] = results[0][1]
        tobs_dict["TAVG"] = results[0][2]
        
        return jsonify(tobs_dict)
 

if __name__ == '__main__':
    app.run(debug=True)
