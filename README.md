## Waste Management App - Backend API

This document describes the API for the waste management application backend written in Flask.

### User Operations

*Register a new user:*

-   URL: /register
-   Method: POST
-   Parameters:
    -   user_data (dict): The data of the user to be registered. It should contain the following keys:
        -   username (str): The username of the user.
        -   password (str): The password of the user.
-   Returns:
    -   dict: A dictionary containing the message "User created successfully".
-   Raises:
    -   409 Conflict: If a user with the same username already exists.

*Log in a user:*

-   URL: /login
-   Method: POST
-   Parameters:
    -   user_data (dict): The data of the user to be logged in. It should contain the following keys:
        -   username (str): The username of the user.
        -   password (str): The password of the user.
-   Returns:
    -   dict: A dictionary containing the message "Login successful" and the access token.
-   Raises:
    -   401 Unauthorized: If the username or password is incorrect.

*Get a user by ID:*

-   URL: /users/{user_id}
-   Method: GET
-   Parameters:
    -   user_id (int): The ID of the user to retrieve.
-   Returns:
    -   UserModel: The user object corresponding to the given ID.
-   Raises:
    -   404 Not Found: If no user with the given ID exists.

*Delete a user by ID:*

-   URL: /users/{user_id}
-   Method: DELETE
-   Parameters:
    -   user_id (int): The ID of the user to delete.
-   Returns:
    -   dict: A dictionary containing the message "User deleted successfully".
-   Raises:
    -   403 Forbidden: If the user does not have admin privileges.
    -   404 Not Found: If no user with the given ID exists.

### Admin Operations

*Get all admins in the database:*

-   URL: /admins
-   Method: GET
-   Authorization: Requires admin privileges.
-   Returns:
    -   dict: A dictionary containing all admins in the database
-   Raises:
    -   Default error response with status code and error details.

*Add a new admin to the database:*

-   URL: /admins
-   Method: POST
-   Authorization: Requires admin privileges.
-   Parameters:
    -   admin_data (dict): A dictionary containing the data for the new admin.
-   Returns:
    -   tuple: A tuple containing the newly added admin and the HTTP status code 201.
-   Raises:
    -   abort: If there is an error adding the admin to the database.

*Get an admin by ID:*

-   URL: /admins/{admin_id}
-   Method: GET
-   Authorization: Requires admin privileges.
-   Parameters:
    -   admin_id (int): The ID of the admin to retrieve
-   Returns:
    -   dict: A dictionary containing the admin with the specified ID
-   Raises:
    -   abort: If there is no admin with the specified ID

*Delete an admin by ID:*

-   URL: /admins/{admin_id}
-   Method: DELETE
-   Authorization: Requires admin privileges.
-   Parameters:
    -   admin_id (int): The ID of the admin to delete
-   Returns:
    -   tuple: An empty tuple and the HTTP status code 204
-   Raises:
    -   abort: If there is no admin with the specified ID

### Households Operations

*Get all households in the database:*

-   URL: /households
-   Method: GET
-   Returns:
    -   dict: A dictionary containing all households in the database
-   Raises:
    -   Default error response with status code and error details.

*Add a new household to the database:*

-   URL: /households
-   Method: POST
-   Parameters:
    -   household_data (dict): A dictionary containing the data for the new household
-   Returns:
    -   tuple: A tuple containing the newly added household and the HTTP status code 201
-   Raises:
    -   abort: If there is an error adding the household to the database
    -   422 Unprocessable Entity: If the request body is invalid

*Get a household by ID:*

-   URL: /households/{household_id}
-   Method: GET
-   Parameters:-   -   household_id (str): The ID of the household to retrieve.
-   Returns:
    -   HouseholdModel: The household object corresponding to the given ID.
-   Raises:
    -   404 Not Found: If no household with the given ID exists.

*Update a household by ID:*

-   URL: /households/{household_id}
-   Method: PUT
-   Parameters:
    -   household_data (dict): A dictionary containing the data to update for the household.
-   Returns:
    -   tuple: A tuple containing the updated household object and the HTTP status code 200.
-   Raises:
    -   404 Not Found: If no household with the given ID exists.
    -   400 Bad Request: If the request body is invalid.

*Delete a household by ID:*

-   URL: /households/{household_id}
-   Method: DELETE
-   Parameters:
    -   household_id (str): The ID of the household to delete.
-   Returns:
    -   dict: A dictionary containing the message "Household deleted successfully".
-   Raises:
    -   404 Not Found: If no household with the given ID exists.

### Waste Items Operations

*Get all waste items in the database:*

-   URL: /waste_items
-   Method: GET
-   Returns:
    -   dict: A dictionary containing all waste items in the database.
-   Raises:
    -   Default error response with status code and error details.

*Add a new waste item to the database:*

-   URL: /waste_items
-   Method: POST
-   Parameters:
    -   waste_item_data (dict): A dictionary containing the data for the new waste item.
-   Returns:
    -   tuple: A tuple containing the newly added waste item and the HTTP status code 201.
-   Raises:
    -   abort: If there is an error adding the waste item to the database.
    -   422 Unprocessable Entity: If the request body is invalid.

*Get a waste item by ID:*

-   URL: /waste_items/{waste_item_id}
-   Method: GET
-   Parameters:
    -   waste_item_id (str): The ID of the waste item to retrieve.
-   Returns:
    -   WasteItemModel: The waste item object corresponding to the given ID.
-   Raises:
    -   404 Not Found: If no waste item with the given ID exists.

*Update a waste item by ID:*

-   URL: /waste_items/{waste_item_id}
-   Method: PUT
-   Parameters:
    -   waste_item_data (dict): A dictionary containing the data to update for the waste item.
-   Returns:
    -   tuple: A tuple containing the updated waste item object and the HTTP status code 200.
-   Raises:
    -   404 Not Found: If no waste item with the given ID exists.
    -   400 Bad Request: If the request body is invalid.

*Delete a waste item by ID:*

-   URL: /waste_items/{waste_item_id}
-   Method: DELETE
-   Parameters:
    -   waste_item_id (str): The ID of the waste item to delete.
-   Returns:
    -   dict: A dictionary containing the message "Waste item deleted successfully".
-   Raises:
    -   404 Not Found: If no waste item with the given ID exists.
