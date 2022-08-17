# COLLECT

This project accepts the forms, questions and responses. We can integrate various servicees which can be invoked on submitting
a response to a form.

### Tech Stack
1. Python3
2. Flask
3. Mongo

### How to Install and Run the Project

1. Install Python3
2. create a virtual env
3. activate virtual env
4. Install dependencies from requirement.txt
5. Keep you config data in .env file
6. For prod use gunicorn, for dev you can directly run `python3 run.py`

### Want to contribute
1. Add new apis in apis package
2. Add new service in services package and add the abstract class 
implementation  in interface.py in services.
3. Add helper fundtions in utils.py
4. If want to add new config, add it in .env file and initialize in settings.py
5. Consumer.py will call sqs queue and initiate related service based on `app_code`
6. Add new database connector or any other service connector in connectors package
