# Hawaii Climate Analysis

### sqlalchemy-challenge
Repository for HW10
by: Arnold Schultz

## Introduction

This is an exercise in using Python and SQLAlchemy to perform basic climate analysis and data exploration of a climate database. This will be done by using SQLAlchemy, ORM queries, Pandas, and Matplotlib.  Once the analysis is done then a Flask server will be created to serve JSON API requests.

In doing this I:

* Used SQLAlchemy’s `create_engine` to connected to the SQLite database.

* Used SQLAlchemy’s `automap_base()` to reflect the tables into classes and saved references to those classes called `stations` and `measurements`.

* Linked Python to the database by creating a SQLAlchemy session.

### Precipitation Analysis

Used session queries and dataframes to get the latest years worth of precipitation data and plotted it using the df.plot() method.
Then the summary statistics of the data was printed.

### Station Analysis

In this area I got a list of all the stations gathering data and found the most active one.  Then looking at the most active station's data gathered both the minimum, maximum and average temperatures as well as the last years worth of temperature observations (tobs).  Lastly I plot a histogram of the observed years worth of temperatures at the most active station.




