## Explanation of Workplace_app
### Why relational?
This is a relational database, this was the best choice for the project because it is well equipt and suited for handling structured data with clear relationships between different entities. Its use of tables, both primary and foreign keys ensures strong data integrity and makes way for fast efficent   querying. Compared to a non relational database this offers a more rigid structure, they are great for flexible and scalable unstructured to semi-structured data but they lack the same level of data integrity and consistency we need, especially with complex transactions. 

For my project a relational database offers well organised and connected data ensuring accuracy, simplified querying and stronger support for the types of transactions need in a workplace and is more well equipt than a non-relational database

### More about the project
This is a workplace relational database, it is used to manage workplace relationships betwee the team so they are able to see their rosters and have those shifts allocated to a specific department. It also manages the projects specific team members are currently working and display which client is commissioning the project,  along with this is feedback the clients have provided about their experiences.

## Publicly accessible URI
https://jacks-workplace-db.onrender.com

## Feedback
### Feedback from Evan

in my model files I was writing my date like this:
```python
  date_submitted = db.Column(db.String(100), nullable=False)
```
using a string which is both inacurate and just incorrect.

I then changed to the following:
```python
    from datatime import date, time

    date_submitted = db.Column(db.Date, nullable=False)
```
This is now more accurate and the correct way of formatting a date in my models files.


### Feedback from a