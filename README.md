My application allows a user to enter their name and save it to a database. This allows someone to see the
all the individuals that have had a chance to use this application. It also allows a user to
enter a screen name (the name involving the @ symbol) for any twitter user and display profile information
about that user. It allows a user to also search for 10, 20, or 30 tweets from a public user.
Additionally, it can display all the users that have been searched and saved to the database
and all the tweets that have been saved to the database.

Although not the best practice, I have left my keys as they are on my midterm.py file.
I trust all of those using grading this. After grading is done I will either delete the project from Github
or modify the code that is there. 

List of Routes and the templates they render:

http://localhost:5000/
Route: /
Renders: home.html

http://localhost:5000/username
Route: username
Renders: userform.html

http://localhost:5000/numtweets
Route: numtweets
Renders: list_tweets.html or numtweets.html depending on if the form validates

http://localhost:5000/list_names
Route: list_names
Renders: name_example.html

http://localhost:5000/list_tweets
Route: list_tweets
Renders: list_tweets.html

http://localhost:5000/list_users
Route: list_users
Renders: list_users.html


**Ensure that the SI364midterm.py file has all the setup (app.config values, import statements, code to run the app if that file is run, etc) necessary to run the Flask application, and the application runs correctly on http://localhost:5000 (and the other routes you set up)**
**Add navigation in base.html with links (using a href tags) that lead to every other viewable page in the application. (e.g. in the lecture examples from the Feb 9 lecture, like this ) **
**Ensure that all templates in the application inherit (using template inheritance, with extends) from base.html and include at least one additional block.**
**Include at least 2 additional template .html files we did not provide.**
**At least one additional template with a Jinja template for loop and at least one additional template with a Jinja template conditional.
  These could be in the same template, and could be 1 of the 2 additional template files.**

**At least one errorhandler for a 404 error and a corresponding template.**
**At least one request to a REST API that is based on data submitted in a WTForm.**
**At least one additional (not provided) WTForm that sends data with a GET request to a new page.**
**At least one additional (not provided) WTForm that sends data with a POST request to the same page.**
**At least one custom validator for a field in a WTForm.**
**At least 2 additional model classes.**
**Have a one:many relationship that works properly built between 2 of your models.**
**Successfully save data to each table.**
**Successfully query data from each of your models (so query at least one column, or all data, from every database table you have a model for).**
**Query data using an .all() method in at least one view function and send the results of that query to a template.**
**Include at least one use of redirect. (HINT: This should probably happen in the view function where data is posted...)**
**Include at least one use of url_for. (HINT: This could happen where you render a form...)**
**Have at least 3 view functions that are not included with the code we have provided. (But you may have more! Make sure you include ALL view functions in the app in the documentation and ALL pages in the app in the navigation links of base.html.)**


Additional Requirements
**(100 points) Write code in your Python file that will allow a user to submit duplicate data to a form, but will not save duplicate data (like the same user should not be able to submit the exact same tweet text for HW3).** This is done when searching for tweets from a user that you've already searched for their tweets before. It will display the data, but does not save it to the db again.
