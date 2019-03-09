# DrinkOrder
A Line bot used in internal organization for counting drink order.

# Features
- A LINE bot.
- Written in Python.
- Uses Flask to build a micro web application.
- Builds application on Heroku.
- Attached Postgres, the add-on of Heroku, as database.
- Through from Flask-Migrate to manage database.

# Installations
1. Install and update **flask**.
```
$ pip install -U Flask
```
2. Install **line-bot-sdk-python**.
```
$ pip install line-bot-sdk
```
3. Install **Flask-Migrate**. Please refer to [Flask-Migrate-Tutorial].

# Deployment
 If you have done programing at local computer, then you can deploy your application on Heroku. Please refer to [Deploying-Flask-To-Heroku]. That tutorial will show you how to deploy on Heroku step by step. In addition, it will teach you how to use Postgres database within Heroku and point you to another tutorial [Flask-Migrate-Tutorial] for teach you create your first data table in database. You can also refer to this tutorial [kamidog-deploy-heroku].


# Requirements
All required packages for run application properly had written in [requirements.txt]. On my experience, the packages version are not absolutely. Maybe you can update the version to latest.

# Links
* [flask] - The Python micro framework for building web applications.
* [line-bot-sdk-python] - SDK of the LINE Messaging API for Python.
* [Flask-Migrate-Tutorial] - A tutorial for manage database through Flask-Migrate.

# License
MIT license

[//]: #

[requirements.txt]:(https://github.com/sa002999/drinkorder/blob/master/requirements.txt)
[flask]:(https://github.com/pallets/flask)
[Flask-Migrate-Tutorial]:https://github.com/twtrubiks/Flask-Migrate-Tutorial
[line-bot-sdk-python]:https://github.com/line/line-bot-sdk-python
[Deploying-Flask-To-Heroku]:(https://github.com/twtrubiks/Deploying-Flask-To-Heroku)
[kamidog-deploy-heroku]:(https://ithelp.ithome.com.tw/articles/10196129)
