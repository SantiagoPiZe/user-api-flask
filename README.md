# Flask User Management API

This is a Python API built with Flask that provides user management functionalities using a MySQL database. It allows you to perform user search, user and organization creation, user assignation to organizations, organization retrieval, and retrieve a call counter value.
Prerequisites

#### Make sure you have the following software installed on your system:

    Python
    MySQL

## Installation

#### Clone the repository:

    git clone https://github.com/SantiagoPiZe/user-api-flask.git
    
#### Setup the database:

Create a new mysql database for the project with the name of your choice. Then inside the project files, locate the .env file and modify:
  
  DB_USERNAME: your mysql username
  DB_PASSWORD: your mysql password
  DB_NAME: the chosen name for the database

#### Inside the project folder, run the following commands:

    - venv/bin/activate
    Activate the virtual enviroment to ensure that the packages are installed within the virtual environment, making them available when you run the project.

    -pip install -r requirements.txt
     This will setup the required dependencies for the project.
    
    -python create_tables.py
     This will run the create_tables.py file that setup the database tables.
     
    -flask run
    This will start the application in localhost:5000

## API Usage

  ### User Endpoints

   #### Search Users
        Method: GET
        Endpoint: /user
        Description: Retrieves a list of users based on specified filters.
        Query Parameters:
            page (optional): Page number for pagination.
            per_page (optional): Number of users per page.
            first_name (optional): Filters users by their first name.
            last_name (optional): Filters users by their last name.
            email (optional): Filters users by their email.
            organization_id (optional): Filters users by the organization ID they belong to.
        Response:
            Body: JSON object containing the list of users matching the filters, total amount of user, current page, and per page amount.

   #### Create User
        Method: POST
        Endpoint: /user
        Description: Creates a new user.
        Request Body:
            JSON  containing user data:
                first_name (required): First name of the user.
                last_name (required): Last name of the user.
                email (required, unique): Email address of the user.
        Response:
            Body: JSON object containing a success message and the created user data.

   #### Assign Organization to User
        Method: POST
        Endpoint: /user/assign_organization
        Description: Assigns a user to an organization.
        Request Body:
            JSON containing user and organization IDs:
                user_id (required): ID of the user.
                organization_id (required): ID of the organization.
        Response:
            Body: JSON object containing a success message.

### Organization Endpoints

   #### Search Organizations
        Method: GET
        Endpoint: /organization
        Description: Retrieves a list of organizations.
        Response:
            Body: JSON object containing the list of all the  organizations.

   #### Create Organization
        Method: POST
        Endpoint: /organization
        Description: Creates a new organization.
        Request Body:
            JSON object containing organization data:
                name (required): Name of the organization.
        Response:
            Body: JSON object containing a success message

### Call Counter Endpoints

   #### Get Call Counter
        Method: GET
        Endpoint: /call_counter
        Description: Retrieves the value of the call counter.
        Response:
            Body: JSON object containing the value of the call counter.

Additional Notes

The API automatically increments a call counter every 5 minutes and logs the value to the console.
