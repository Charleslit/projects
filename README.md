Rent App Documentation

The Rent App is a simple Flask web application that allows users to keep track of their rent payments. The application has the following features:
User Authentication

The Rent App supports user authentication, which allows users to create an account, log in, and log out. User authentication is implemented using the Flask-Login extension.
Rent Payment Management

The Rent App allows users to record their rent payments. Users can add a new rent payment by providing the following information:

    Amount: The amount paid for rent
    Name: The name of the landlord or property manager
    Date: The date on which the payment was made

The Rent App also allows users to view all of their rent payments, as well as edit or delete existing payments.
Rent Balance Calculation

The Rent App calculates the rent balance for each user based on their rent payments. The rent balance is the difference between the total amount of rent owed and the total amount of rent paid.
User Rent Information Display

The Rent App allows users to view their rent information including the total amount of rent paid and their rent balance.
Admin Rent Information Display

The Rent App allows admin users to view rent information for all users including the latest amount paid and their total amount paid.
Dependencies

The Rent App is built on the following dependencies:

    Flask
    Flask-Login
    Flask-WTF
    SQLAlchemy

Getting Started

To run the Rent App, follow these steps:

    Clone the repository from GitHub.
    Create a virtual environment and activate it.
    Install the required dependencies using the command pip install -r requirements.txt.
    Set the environment variable FLASK_APP to run.py.
    Initialize the database using the command flask db upgrade.
    Start the server using the command flask run.

Conclusion

The Rent App is a simple Flask web application that allows users to keep track of their rent payments. It provides basic rent management functionalities and can be easily extended to support more advanced features.



 


