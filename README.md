# Key Value Store
This app is a basic key-value store.
* JSON REST API using Flask-Restless
* Bootstrap frontend for getting/setting values

## Assumptions
* Keys and values can be any unicode strings
* The value for a key cannot be overwritten once it is set

## Running the App
* Make sure you're on python3
* Install python packages
```
$ pip install -r requirements.txt
```
* Run the flask app:
```
$ export FLASK_APP=run.py
$ flask run
```
* View the app in the browser at http://127.0.0.1:5000

## Running Tests
```
python tests.py
```

## Further Work
* Make production-ready
  * Add settings toggle for running in production vs staging vs local
  * Use a better database (e.g. PostgreSQL)
  * Consider adding metrics on latency and DB query time
  * Consider adding logging
* As the application gets bigger, organize files better instead of everything in the one `key_value_store.py` file
* Surface duplicate key validation error in API response instead of 
the generic "Could not determine specific validation errors" validation 
error. See TODO in `test_set_duplicate_key`.
* Improve the UI
  * Get rid of the alert boxes
  * Consider bootstrap alerts for errors
  * Consider bootstrap modals for displaying results