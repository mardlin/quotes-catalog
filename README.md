## Synopsis

A repository of quotations, organized thematically. I built this for Project 3 of the Udacity Fullstack Nanodegree. The project is focused on backend code, not prettiness. 

NB for the Udacity Reviewer: the namespace of the front end of this site is organize by themes>quotes. The backend is in keeping with the catalog app created in the related course, and the namespace is organize by categories>items

## Installation

Setup the database:
`$ python database_setup.py`

Populate the database:
`$ python populate_database.py`

Run: 
`$ python project.py` 

In your browser visit http://0.0.0.0:5000 to view the site. 

## Usage:

- The site is read only unless logged in via Google Plus's OAuth2.0
- When logged in, you can add any quotes you'd like to the category of your choice. 
- You can also edit or delete any of the quotes you've created. Other contributor's quotes can't be edited. 

## API

There are three JSON endpoints for retrieving quotes:

1. /themes/json
2. /themes/[category_name]/json
3. /themes/[category_name]/[item_name]/json