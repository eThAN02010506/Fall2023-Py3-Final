# Fall 2023 Python 3 Final

*For the final, you will be completing the **ttkbootstrap** application. Currently, the application has very basic navigation and widgets on the screen. You will complete it and add your own data to it.*

##### Installation Steps:

+ Fork the repo
+ Clone the repo to your local machine

##### Rubric:

+ Your application should consume your API (either the custom one you made or the tasks one we made in class)
+ Your router for the application should meet the following specifications:
  + Have all CRUD operations accounted for (POST, GET, PUT, DELETE)
  + Require authentication in order to access it
  + Data should be stored in a SQLite database
  + Data table contains a foreign key to identify the user each row belongs to
+ Your UI should adopt the information it gets from the database

##### Grade Breakdown

+ 75%: Rubric Requirements Met
+ 25%: UI Design

**Special Note about your UI Design: The documentation has examples of multiple ways to implement widgets and designs, use them. The more creative the result, the better your grade.*


About my UI: 
It allows to create a user, and to use the email and password to log in. For each usre, the display is different
so that user can only see the tasks they created and edit. Click on update will allow user to look at specific description
A default user is already set: admin, psd: admin. 
The database is stored using json, in the API. everytime, this request from the API, and displays returned value.
