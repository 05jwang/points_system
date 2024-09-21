Points System
=============
This project is a Django-based REST API with a SQLite database that handles a points based rewards system for a single user account. Points are credited by a payer and are deducted in order of the oldest points first. It was created by Jerry Wang (05jwang@gmail.com) as a coding challenge for Fetch Rewards.

API Endpoints
-------------
- `POST /add`
    - Credits points to the user account
    - Request body:
    ```
    {
        "payer": STRING,
        "points": INTEGER,
        "timestamp": STRING (ISO 8601 format)
    }
    ```
    - Response body:
        None
- `POST /spend`
    - Deducts points from the user account, in a FIFO (first-in, first-out) manner
    - Request body:
    ```
    {
        "points": INTEGER
    }
    ```
    - Response body:
    ```
    [
        {
            "payer": STRING,
            "points": INTEGER
        } 
        ... (for each payer)
    ]
    ```
- `GET /balance`
    - Retrieves the current balance of points in the user account, by payer
    - Request body:
        None
    - Response body:
    ```
    {
        payer: amount,
        ... (for each payer)
    }
    ```

Getting Started
===============

Dependencies
------------
- [git](https://git-scm.com/downloads)
- [Python 3](https://www.python.org/downloads/)
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)

Installation
------------
To start, open up a terminal. A terminal can be opened by pressing `Win + R` and typing `cmd` on Windows, `Cmd + Space` and typing `Terminal` on MacOS, or `Ctrl + Alt + T` on Linux. Then run the following commands:
1. Clone the repository
```
git clone https://www.github.com/05jwang/points_system.git
```
2. Change directory to the project folder
```
cd points_system
```
3. Create a virtual environment
A virtual environment isolates the dependencies of the project from the system dependencies. Create a virtual environment by running the following command:
```
python3 -m venv venv
```
4. Activate the virtual environment
    - Windows
    ```
    .\venv\Scripts\activate
    ```
    - MacOS/Linux
    ```
    source venv/bin/activate
    ```
When the virtual environment is activated, the terminal prompt should change to show `(venv)` before the command prompt.
5. Install dependencies
```
pip3 install -r requirements.txt
```
6. Set up the database
This project uses SQLite as the database. To set up the database, run the following command:
```
python3 manage.py migrate
```
7. Run the server
```
python3 manage.py runserver
```
You should see output with the following:
```
Starting development server at http://127.0.0.1:8000/
```
8. Run tests (optional)
```
python3 manage.py test
```

The server is now running. You can access the three API endpoints at the following URLs:
- `POST /add`: http://localhost:8000/add
- `POST /spend`: http://localhost:8000/spend
- `GET /balance`: http://localhost:8000/balance
To stop the server, press `Ctrl + C` in the terminal. To deactivate the virtual environment, run the following command:
```
deactivate
```


Summary
=======
[Summary](summary.txt)