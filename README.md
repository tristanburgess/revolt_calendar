## Table of contents

* [Intro](#revolt-calendar)
* [Quick start](#getting-started)
* [What's Included](#whats-included)
* [Creators](#creators)

## Revolt Calendar
This app provides a full stack solution for displaying a single-day event
calendar. This is a REVOLT exclusive :)

![alt-tag](http://i.imgur.com/R0lkGNz.png)

## Getting started

Requirements:

* Python version 2.7.11 or greater.
* python-pip
* python-flask 
* python-sqlalchemy
* requests
* httplib2

Here's how to get started (with Linux):

* [Download the latest release](https://github.com/tristanburgess/revolt_calendar/archive/master.zip) OR
* Clone the repo: `git clone https://github.com/tristanburgess/revolt_calendar.git`
* Navigate to the directory where you have downloaded the repo, and unzip if necessary
* Install dependencies:
    * apt-get -qqy install python python-flask python-sqlalchemy
    * apt-get -qqy install python-pip
    * pip install requests
    * pip install httplib2
* Create the app database: python db_setup.py
* Start the app server: python revolt_calendar.py
* Connect via localhost: http://localhost:5000
* Add a dataset
    * Use a JSON file that follows the following format. You can find example files in the tests dir:
    ![alt-tag](http://i.imgur.com/II2Mswa.png)
    * Upload your JSON file and give it a name:
    ![alt-tag](http://i.imgur.com/bUFut0W.png)
    * Select the dataset from the list and click "Render Calendar!":
    ![alt-tag](http://i.imgur.com/HJ25vgg.png)
    * You can also view the JSON endpoint for any event by clicking on the event's title in the calendar:
    ![alt-tag](http://i.imgur.com/4tFLQy5.png)
    ![alt-tag](http://i.imgur.com/T2jspjE.png)

## What's included

Within the download, you'll find the following files of interest:

```
worksack/
├── models/ - contains DB definitions
├── static/ - contains css and image files
├── templates/ - contains the site's data-driven html pages
├── tests/ - contains test cases I used to validate app functionality
├── revolt_calendar.py - provides the app backend
├── db_setup.py - initializes the SQL alchemy + SQLite database
```


## Creators

**Tristan Burgess**

* <https://www.linkedin.com/in/tristanburgess1>
* <https://github.com/tristanburgess>
