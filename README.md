[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

  <h3 align="center">The API for a social networking application</h3>

### Functional requirements:
* There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..);
* As a user I need to be able to sign up and login;
* As a user I need to be able to create, edit, delete and view posts;
* As a user I can like or dislike other users’ posts but not my own;
* The API needs a UI Documentation (Swagger/ReDoc);

### Technology stack:
* FastAPI
* PostgreSQL
* Poetry

### Installation:
* Clone the repository to a local directory:
  ```sh
  git clone https://github.com/Stanis96/mini_blog_api.git
  ```
* Activating the virtual environment and installing dependencies:
  ```sh
  poetry config virtualenvs.in-project true
  poetry install
  ```
* At the root of the project, create ```.env``` and set the values of the variables:
    ```sh
    POSTGRES_USER=
    POSTGRES_PASSWORD=
    POSTGRES_SERVER=#localhost
    POSTGRES_PORT=#5432
    POSTGRES_DB=
    ```
