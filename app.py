# import libraries
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt


# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite?check_same_thread=False")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)



# Create app
app = Flask(__name__)


# Set routes
@app.route("/")
def links():
    return (
        "List of routes available for this website!</br></br>"
        "/api/v1.0/precipitation</br>"
        "/api/v1.0/stations</br>"
        "/api/v1.0/tobs</br>"
        "/api/v1.0/'start date as YYYY-MM-DD'</br>"
        "/api/v1.0/'start date as YYYY-MM-DD'/'end date as YYYY-MM-DD'</br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    qry = session.query(Measurement.date, func.sum(Measurement.prcp).\
    label("prcp")).\
    group_by(Measurement.date).\
    order_by(Measurement.id.desc()).\
    limit(365).\
    all()

    precipitation = []
    for rain in qry:
        rain_dict = {}
        rain_dict[rain.date] = rain.prcp
        precipitation.append(rain_dict)

    return jsonify(precipitation)



@app.route("/api/v1.0/stations")
def stations():

    qry = session.query(Station).\
    all()

    station_list = []
    for station in qry:
        station_dict = {}
        station_dict["station"] = station.station
        station_dict["name"] = station.name
        station_list.append(station_dict)
    
    return jsonify(station_list)



@app.route("/api/v1.0/tobs")
def temperature():

    last_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).\
    first()

    year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    qry = session.query(Measurement.tobs).\
    filter(Measurement.date >= year_ago).\
    all()

    temps_list = []
    for temp in qry:
        temp_dict = {}
        temp_dict["temp"] = temp.tobs
        temps_list.append(temp_dict)
    
    return jsonify(temps_list)


@app.route("/api/v1.0/<start>")
def temp_start(start=''):
    
    min_t = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()
    max_t = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()
    avg_t = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    all()

    min_str = str(min_t[0][0])
    max_str = str(max_t[0][0])
    avg_str = str(avg_t[0][0])
    
    temps_summary = {
            'Min': min_str,
            'Max': max_str,
            'Avg': avg_str
    }
    
    return jsonify(temps_summary)



@app.route("/api/v1.0/<start>/<end>")
def temp_range(start="",end=""):
    
    min_t = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()
    max_t = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()
    avg_t = session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date >= start).\
    filter(Measurement.date <= end).\
    all()

    min_str = str(min_t[0][0])
    max_str = str(max_t[0][0])
    avg_str = str(avg_t[0][0])

    temps_summary = {
            'Min': min_str,
            'Max': max_str,
            'Avg': avg_str
    }
    
    return jsonify(temps_summary)


if __name__ == '__main__':
    app.run(debug=True)