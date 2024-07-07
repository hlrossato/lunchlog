# LunchLog

**Disclaimer:** _This project is intended for test and local usage and it's not production ready._

## Assumptions and Important Notes
- Upon starting the project, a basic .env will be created automatically (can be seen in loadenv.py file).

- Given this project uses AWS S3 and Google Places API, it's important that all secrets and credentials needed are provided. The project assumes they following keys will be provided:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - GOOGLE_PLACES_API_KEY

    Those secrets and credentials needs to be stored in the .env file.

## How to run the project

The project is built using `Docker` and `Docker-compose` and all the commands needed to run everything on the project can be found in the `Makefile`.

In order to run the project some steps must be followed. Please find the steps and explanation to those below:

- To build the containers, please run `make docker-build-up`
- On another terminal tab/window, run `make migrate` so the database can be created.
- For creating a `Django Superuser`, please run `make superuser`. You can access the Django Admin page through http://localhost:8000/admin

## Access to the APIs
The API can be access through the standard Django REST Framework page and the urls for it are the following:
* [SignUp - http://localhost:8000/auth/signup](http://localhost:8000/auth/signup)
* [Login - http://localhost:8000/auth/login](http://localhost:8000/auth/login)
* [Receipts - http://localhost:8000/receipts/](http://localhost:8000/receipts/)
* [Receipt Detail - http://localhost:8000/receipts/{uuid}](http://localhost:8000/receipts/<uuid>)
    * A receipt UUID must be provided for this endpoint to work
* [Food Recommendation - http://localhost:8000/recommendations](http://localhost:8000/recommendations)
    * The page will return an empty list if no city is provided through the filters button

## How to run the tests

The tests were written using `pytest` and can be run as follows:
* `make tests` - Run all the tests
* `make tests TEST=/path/to/test.py` - Run the selected test
* `make tests-cov-report` - Run tests generating html reports

For more commands, please check the `Makefile`

## Documentation
The documentation for this project are comprised of the [API Schemas](http://localhost:8000/api/schema/swagger-ui/#/) and a DB graph, called [LunchLog.png](docs/out/docs/class-diagram/LunchLog.png). The [class-diagram](docs/class-diagram.puml) file that generated this graph can also be seen under `docs` folder.

## Lessons learned
I had the opportunity to integrate and consume the Google Places API which I had never touched before and although it was a basic implementation, I found it really fun to do. I also found a couple of third-party packages that did that integration but decided to write a simpler solution.

Although I knew by name, I had never used `poetry` before and it was defintely a fun experience to work with it. I found it to be simpler than I initially though.

I also decided to use Github Actions which was pretty straight forward to integrate and run.

And last but not least, I found `mypy` can be a bit tricky to work with `:D`
