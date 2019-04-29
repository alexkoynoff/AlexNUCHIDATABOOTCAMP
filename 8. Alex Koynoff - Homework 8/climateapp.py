from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import datetime as dt

########################################
# Database Set up
########################################

engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
session = Session(engine)

# Save references to the tables
Station = Base.classes.station
Measurement = Base.classes.measurement

########################################
# Flask Set up
########################################
app = Flask(__name__)

########################################
# Flask Routes
########################################

@app.route("/")
def welcome():
    return(
        f'Available Routes: <br/>'
        f'/api/v1.0/precipitation'
        f' - Provides information for precipitation. <br/>'
        f'/api/v1.0/stations' 
        f' - Lists the available stations. <br/>'
        f'/api/v1.0/tobs'
        f' - Provides information for temperature observations. <br/>'
        f'/api/v1.0/yyyy-mm-dd'
        f' - Enter start date in the link above with this format: yyyy-mm-dd <br/>'
        f'/api/v1.0/yyyy-mm-dd/yyyy-mm-dd'
        f' - Enter start date AND end date in the link above with this format: yyyy-mm-dd <br/>'
        
    )


@app.route("/api/v1.0/precipitation")
def pcrp():
    precipitation=session.query(Measurement.date, Measurement.prcp, Measurement.station).filter(Measurement.date.between("2016-08-23", "2017-08-23")).all()

    pcrp_list=[]
    for pcrp in range(len(precipitation)):
        prcp_dict = {}
        prcp_dict["date"] = precipitation[pcrp][0]
        prcp_dict["prcp"] = precipitation[pcrp][1]
        prcp_dict["station"] = precipitation[pcrp][2]
        pcrp_list.append(prcp_dict)

    return jsonify(pcrp_list)


#############################################

@app.route("/api/v1.0/stations")
def stations():
   
    # Query all stations from the station table
    station_results = session.query(Station.station, Station.name).group_by(Station.station).all()

    station_list = list(np.ravel(station_results))
    return jsonify(station_list)

##############################################

@app.route("/api/v1.0/tobs")
def tobs():
    temperature=session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date.between("2016-08-23", "2017-08-23")).all()

    tobs_list=[]
    for temp in range(len(temperature)):
        tobs_dict = {}
        tobs_dict["date"] = temperature[temp][0]
        tobs_dict["temp"] = temperature[temp][1]
        tobs_dict["station"] = temperature[temp][2]
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

#start date
@app.route("/api/v1.0/<start_date>/")
def temp_start(start_date):
    
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).first()
    
    temps_dict1 = {"minimum temperuture": temps[0], "maximum temperature": temps[1], "average temperature": round(temps[2],2)}
    return jsonify(temps_dict1)

#start/end date
@app.route("/api/v1.0/<start_date>/<end_date>/")
def temp_range(start_date, end_date):
    
    temps = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date.between(start_date, end_date)).first()
    
    temps_dict2 = {"TMIN": temps[0], "TMAX": temps[1], "TAVG": round(temps[2],2)}
    return jsonify(temps_dict2)


    

if __name__ == '__main__':
    app.run(debug=True)