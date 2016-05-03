import os
import random
import string
import httplib2
import json
import requests
from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash
from models.event import Event
from models.event_type import EventType
from models.input_set import InputSet
from app import app
from session import session

APPLICATION_NAME = "RevoltCalendar"
ALLOWED_EXTENSIONS = set(['json'])

def validFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/event/<int:event_id>/JSON/')
def eventJSON(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    return jsonify(event.serialize)

# Dashboard
@app.route('/')
@app.route('/dashboard/')
def showDashboard():
    """Gathers the users categories and tasks, and renders the dashboard page.

    Returns:
      The dashboard page state
    """
    inputSets = session.query(InputSet).all()
    return render_template('dashboard.html', inputSets=inputSets)

# Calendar
@app.route('/calendar/', methods=['GET', 'POST'])
def renderCalendar():
    """Gets all events attached to the selected input set, and then renders the
    event calendar utilizing the selected data. The frontend logic for the 
    calendar is contained in templates/static.html

    Returns:
      The rendered calendar template if POST, otherwise returns to the dashboard.
    """
    if request.method == 'POST':
        inputSetId = request.form["inputSet"]
        if (inputSetId is None):
            flash("Please upload and select a valid input set.")
            return redirect(url_for('showDashboard'))
        events = session.query(Event).filter_by(input_set_id=inputSetId).all()
        return render_template('calendar.html', events=events)
    return redirect(url_for('showDashboard'))


@app.route('/source/')
def showSource():
    """
    Returns:
      Redirect to GitHub repo link
    """
    return redirect("https://github.com/tristanburgess/revolt_calendar")


@app.route('/about/')
def showAbout():
    """
    Returns:
      Redirect to my LinkedIn page.
    """
    return redirect("http://www.linkedin.com/in/tristanburgess1")

@app.route('/upload_events/', methods=['GET', 'POST'])
def uploadEvents():
    """Attempts to parse and store a JSON file sent in the request.
        Every file uploaded is considered as an input set, which is a set of data
        that provides a complete test case for the app's main functionality.
        
    Returns:
      The dashboard page state with message flashes on error.
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and validFile(file.filename):
            try:
               events = json.load(file)
            except:
                flash("An error occurred while parsing the provided JSON. Please check the validity of the data.")
                return redirect(url_for('showDashboard'))

            try:
                inputSet = InputSet(name=request.form["name"])
                session.add(inputSet)
                session.commit()
            except:
                session.rollback()
                flash("Input set could not be added successfully.")
                return redirect(url_for('showDashboard'))

            for event in events:
                try:
                    eventType = session.query(EventType).filter_by(name=event["type"]).one()
                    
                    # Ensure that start and endtimes are stored as timestamps
                    # with no corresponding date.
                    startTime = datetime.strptime(event["startTime"], "%H:%M:%S").time()
                    endTime = datetime.strptime(event["endTime"], "%H:%M:%S").time()
                    
                    dbEvent = Event(title=event["title"], description=event["description"], 
                                    startTime=startTime, endTime=endTime, address=event["address"], 
                                    type_id=eventType.id, input_set_id=inputSet.id)

                    session.add(dbEvent)
                    session.commit()
                except:
                    session.rollback()
                    flash("An error occurred while saving the JSON. Please check the validity of the data.")
                    return redirect(url_for('showDashboard'))
               
            return redirect(url_for('showDashboard'))
        else:
            flash("A JSON file was not provided. Nothing to see here...")
    return redirect(url_for('showDashboard'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = False
    app.run(host='0.0.0.0', port=5000)
