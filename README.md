[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Build Status](https://github.com/Stanis96/social_network_api/actions/workflows/test_linter.yml/badge.svg?branch=main)
<h1 align="center">The API for a social networking application</h1>

### Сompleted tasks:
* There should be some form of authentication and registration (JWT, Oauth, Oauth 2.0, etc..);
* As a user I need to be able to sign up and login;
* As a user I need to be able to create, edit, delete and view posts;
* As a user I can like or dislike other users’ posts but not my own;
* The API needs a UI Documentation (Swagger/ReDoc);

### Preview:
![](app/static/preview.gif)

### Installation:
* Clone the repository to a local directory:
  ```sh
  git clone https://github.com/Stanis96/mini_blog_api.git
  ```
* Set your own variable values in ```.env_template``` and rename to ```.env```
>Tip: The application uses a third-party PostgreSQL database service.
* Application launch:
```sh
  docker-compose -f docker-compose.yaml up --build
  ```
>Swagger UI:
> >http://localhost:8000/docs

>ReDoc:
> >http://localhost:8000/redoc
* Local testing:
```sh
  docker-compose -f docker-compose-local.yaml up --build
  ```
### Endpoints info:
| Router                        | Description                      |
|:------------------------------|:---------------------------------|
| POST/users/create             | Creating a new user              |
| GET/users/show_all            | Returns data for all saved users |
| GET/users/show_user           | Returns your user data           |
| GET/users/{email}             | Search users by email            |
| POST/singin/                  | Creation of a personal token     |
| POST/posts/create             | Creating a new post              |
| GET/posts/show_all            | Returns data for all saved posts |
| GET/posts/show/{post_id}      | Search users by id of post       |
| PUT/posts/update/{post_id}    | Updating own posts               |
| DELETE/posts/delete/{post_id} | Deleting onw posts               |
| POST/posts/like/{post_id}     | Like post only other users       |
| POST/posts/dislike/{post_id}  | Disike post only other users     |

>Tip: All actions are possible only after authorization.
