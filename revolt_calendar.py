import os
import random
import string
import httplib2
import json
import requests
from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, make_response
from models.event import Event
from models.event_type import EventType
from models.input_set import InputSet
from app import app
from session import session

APPLICATION_NAME = "RevoltCalendar"
ALLOWED_EXTENSIONS = set(['json'])

def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/event/<int:event_id>/JSON')
def eventJSON(event_id):
    events = session.query(Event).filter_by(id=event_id).all()
    return jsonify(Event=[event.serialize for event in events])

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
    """Gathers the users categories and tasks, and renders the dashboard page.

    Returns:
      The dashboard page state
    """
    if request.method == 'POST':
        inputSetId = request.form["inputSet"]
        events = session.query(Event).filter_by(input_set_id=inputSetId).all()
        return render_template('calendar.html', events=events)
    return redirect(url_for('showDashboard'))


@app.route('/source/')
def showSource():
    """
    Returns:
      Redirect to GitHub repo link
    """
    return redirect("https://github.com/tristanburgess/")


@app.route('/about/')
def showAbout():
    """
    Returns:
      Redirect to my LinkedIn page.
    """
    return redirect("http://www.linkedin.com/in/tristanburgess1")

@app.route('/upload_events/', methods=['GET', 'POST'])
def uploadEvents():
    if request.method == 'POST':
        file = request.files['file']
        if file and valid_file(file.filename):
            inputSet = InputSet(name=request.form["name"])
            session.add(inputSet)
            session.commit()
            
            events = json.load(file)
            for event in events:
                eventType = session.query(EventType).filter_by(name=event["type"]).one()
                startTime = datetime.strptime(event["startTime"], "%H:%M:%S").time()
                endTime = datetime.strptime(event["endTime"], "%H:%M:%S").time()
                dbEvent = Event(title=event["title"], description=event["description"], startTime=startTime, endTime=endTime, address=event["address"], type_id=eventType.id, input_set_id=inputSet.id)
                session.add(dbEvent)
                session.commit()
                
            return redirect(url_for('showDashboard'))
    return redirect(url_for('showDashboard'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
