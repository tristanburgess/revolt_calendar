import os
import random
import string
import json
from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash
from models.event import Event
from models.event_type import EventType
from models.input_set import InputSet
from app import app
from session import session

APPLICATION_NAME = "revolt_calendar"
ALLOWED_EXTENSIONS = set(['json'])

def valid_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/event/<int:event_id>/JSON/')
def event_JSON(event_id):
    event = session.query(Event).filter_by(id=event_id).one()
    return jsonify(event.serialize)

# Dashboard
@app.route('/')
@app.route('/dashboard/')
def show_dashboard():
    """Gathers the users categories and tasks, and renders the dashboard page.

    Returns:
      The dashboard page state
    """
    input_sets = session.query(InputSet).all()
    return render_template('dashboard.html', input_sets=input_sets)

# Calendar
@app.route('/calendar/', methods=['GET', 'POST'])
def render_calendar():
    """Gets all events attached to the selected input set, and then renders the
    event calendar utilizing the selected data. The frontend logic for the 
    calendar is contained in templates/static.html

    Returns:
      The rendered calendar template if POST, otherwise returns to the dashboard.
    """
    if request.method == 'POST':
        input_set_id = request.form["inputSet"]
        if (input_set_id is None):
            flash("Please upload and select a valid input set.")
            return redirect(url_for('show_dashboard'))
        events = session.query(Event).filter_by(input_set_id=input_set_id).all()
        return render_template('calendar.html', events=events)
    return redirect(url_for('show_dashboard'))


@app.route('/source/')
def show_source():
    """
    Returns:
      Redirect to GitHub repo link
    """
    return redirect("https://github.com/tristanburgess/revolt_calendar")


@app.route('/about/')
def show_about():
    """
    Returns:
      Redirect to my LinkedIn page.
    """
    return redirect("http://www.linkedin.com/in/tristanburgess1")

@app.route('/upload_events/', methods=['GET', 'POST'])
def upload_events():
    """Attempts to parse and store a JSON file sent in the request.
        Every file uploaded is considered as an input set, which is a set of data
        that provides a complete test case for the app's main functionality.
        
    Returns:
      The dashboard page state with message flashes on error.
    """
    if request.method == 'POST':
        file = request.files['file']
        if file and valid_file(file.filename):
            try:
               events = json.load(file)
            except:
                flash("An error occurred while parsing the provided JSON. Please check the validity of the data.")
                return redirect(url_for('show_dashboard'))


            try:
                input_set = InputSet(name=request.form["name"])
                session.add(input_set)

                for event in events:
                    event_type = session.query(EventType).filter_by(name=event["type"]).one()
                    
                    # Ensure that start and endtimes are stored as timestamps
                    # with no corresponding date.
                    start_time = datetime.strptime(event["startTime"], "%H:%M:%S").time()
                    end_time = datetime.strptime(event["endTime"], "%H:%M:%S").time()
                    
                    db_event = Event(title=event["title"], description=event["description"], 
                                    start_time=start_time, end_time=end_time, address=event["address"], 
                                    type_id=event_type.id, input_set_id=input_set.id)

                    session.add(db_event)

                session.commit()
            except:
                session.rollback()
                flash("An error occurred while saving the provided JSON. Please check the validity of the data.")
                return redirect(url_for('show_dashboard'))

            return redirect(url_for('show_dashboard'))
        else:
            flash("A JSON file was not provided. Nothing to see here...")
    return redirect(url_for('show_dashboard'))

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
