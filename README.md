## Pre-requisites:
* Create a Github account if you don’t have one.
* If you don’t have Git installed in your computer,  install Git using this guide. [Git - Installing Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
* This a template repository. So, you will fork this repository in your GitHub account before working on it. This will give you a complete ownership of your code. To fork this project, click on the Fork button on the top right corner.
* Once you have the forked project, you will clone it to your computer to get started. To clone the project, click on the green “Clone or Download” button and follow the instructions.
* Learn about GitHub and Git commands. We will use git throughout the program, so make sure you have basic understanding of GIT.
* We will use Visual Studio Code as a text editor. If you have a different preference like PyCharm, Sublime Text, Atom etc., feel free to stick with it. Install [Visual Studio Code](https://code.visualstudio.com/) 
* If you don’t have npm installed in your computer,  install npm using this guide. [Npm - get npm](https://www.npmjs.com/get-npm)


# Django Server
This is the repo for Online Payment Server. We use Python, Django Framework and Django Rest Framework. For the database, we are using MYSQL.


### Development Environment Setup

##### Download and install the tools
1. VirtualBox [Download Here.](https://www.virtualbox.org/)
2. Vagrant [Download Here.](https://www.vagrantup.com/downloads.html)

##### Setup the Project
1. Open terminal, go inside your project directory and run the vagrant machine: `npm run vagrant`
2. Install npm in your virtual environment: `sudo apt-get install nodejs npm`
3. Run the setup script: `npm run setup`
4. Run the Django server: `npm run server`

### Development
For the development, you will need to run the Django Server to test the apis as you code them. Here are some important instructions:

#### Running Django App
We will always run our Django App in the Linux Machine inside the virtual environment we initially created. Why? So, that our app doesn't break as dependencies on your local machine (eg. python) gets updated. To run the django server:

1. Open terminal, go inside your project directory and run the vagrant machine: `npm run vagrant`
2. Run the Django server: `npm run server`

#### Creating new Django App
Every set of feature is treated as a new Django App. A Django project can have many Django apps (Eg. Authentication, Profile, Payment etc.). If you are working on a set of APIs for a new feature, create a new Django app inside the folder apps. 

`npm run createapp <app-name>`

Once you create a new app, you have to enable the app in the project. To enable a newly created app, go to your project directory `django-server` and in the `settings.py` file, add your new app in the `INSTALLED_APPS` array.

#### Migrations
Migrations in Django are a way of propagating changes made in the model into the database schema. A migration creates, updates or deletes tables in the database based on the model changes. Some useful commands for migrations are:

##### Generate migrations for a Django App
When you create a new app and add models to it, you will need to generate the migration files for that particular app. To generate migration files, run the following command: <br/>
`npm run createmigration <app-name>`
<br/>

##### Run the migrations
Once the migration files are created, we must run them to apply changes to the database. To run all migrations, run the following command:

`npm run migrate`

###### If port is taken or unavailable, you can free up the port by killing the process:
`npm run kill`

###### If you installed any new package, add it to the requirements.txt:
`npm run save`

<br/>
###### Happy Development!
