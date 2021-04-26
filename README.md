# log-handler
Test assignment for GRAFFIT

![Workflow status](https://github.com/ouriso/log-handler/actions/workflows/workflow.yaml/badge.svg)

## Install
To run the application locally, you need to install a virtual environment  
`python -m venv {venv}` or `virtualenv {venv}` (for example)  
and dependencies:
`pip install -r requirements.txt`

## About
The app makes get request by url 'http://www.dsdev.tech/logs/' (by default)  
and saves parsed data to DB (sqlite by default)  
The main file is `log_handler.py`
The rest of the files perform the following functions:  
`db_settings.py` - settings for SQLAlchemy ORM  
`models.py` - creation and description of tables for DB (ORM)  
`utils.py` - additional functions  

## Running
To run the app execute the file `log_handler.py` from app dir:  
`python -m app.log_handler.py`

or import the Log_handler class from this file:  
`from app.log_handler import Log_handler`  
`instance = Log_handler(date) # str format of 'date' is '%Y-%m-%dT%H:%M:%S'`  
`instance.get_logs()`  