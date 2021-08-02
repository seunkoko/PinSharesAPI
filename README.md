# PinSharesAPI

API for Map location sharing website. Find out more info [here](https://github.com/seunkoko/PinShares).

Hosted on heroku [here](https://pin-shares-api.herokuapp.com/)

### Features
---

* Users can create an account.
* Users can login to their account.
* Users can get their info including their `Added Pins`, `Shared Pins` and `All Pins`.
* Users can get all other users on the platform.
* Users can add pin.
* Users can update their pin.
* Users can share pins with other users.

**Authorization**:
Users are authorized by using JSON web token (JWT).
By generating a token on registration and login, API endpoints are protected from unauthorized access.
Requests to protected routes are validated using the generated token.

### Endpoints
---

This is the [link](https://pin-shares-api.herokuapp.com/) in which to access the api. 

Below are the collection of routes.


#### Routes
EndPoint          |   Functionality    |    Request body/params
------------------|--------------------|--------------------------------------------------------------
POST /signup     | Create a user account   | body [username (string), password (string)]
POST /login       | Logs in a user    | body [username (string), password (string)]        
GET /user_info      | Gets a user's info along with pins     | *token
GET /all_users      | Gets all users    | *token
POST /pin | Creates pin | *token, body [name (string), latLng (array)]
PUT /pin/:pin_id     | Edit pin  | *token, body [name (string), latLng (array)]
POST /share_pin/:pin_id  | Share pin | *token, body [user_ids (array)]


### Technologies Used
---

- Python
- Flask
- Flask-Restful
- Flask-Sqlalchemy
- Flask-Marshmallow
- Flask-JWT
- Postgresql


### Installation
---

- Clone the project repository.
- Run git clone https://github.com/seunkoko/PinSharesAPI.git.
- Change directory into the PinSharesAPI directory.
- Create a virtual environment for the python app. You can refer to this [link](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/).
- Activate your vitual environment.
- Install all necessary packages in the requirements.txt file. You can use the command `pip3 install -r requirements.txt`.
- Create your postgres database. You can checkout [ElephantSql](https://www.elephantsql.com/) or create a database locally.
- Set up your environment variable. Checkout `.env.sample`  in the root folder to do this.
- Export your FLASK_APP `server.py`.
- Upgrade your database by running `python3 manage.py db upgrade`.
> Note: You do not need to initialize and run migrations because there is a migrations folder already in the application `./migrations`.
- To start your app locally, run `python3 server.py`.
- Use Postman or any API testing tool of your choice to access the endpoints defined above.
- To run tests, run `pytest -v`.


#### Contributing
---

1. Fork this repository to your account.
2. Clone your repository: git clone https://github.com/seunkoko/PinSharesAPI.git.
4. Commit your changes: git commit -m "did something".
5. Push to the remote branch: git push origin new-feature.
6. Open a pull request.


### Future Futures
---
-

Copyright (c) 2021 Oluwaseun Owonikoko
