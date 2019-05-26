# Facebook Messenger / Goodreads, recommendations bot

## Project setup

Create a `.env` file and edit the environments variables values for Facebook, Goodreads, and optional Redis setup.

The sessions module uses a Redis database instance, you can run a local Redis instance using Docker. Open a command line console and execute this command:
```
docker run -d -p 6379:6379 --name my-redis redis
```

The default Redis session setup is:
```
SESSION_REDIS_HOST=localhost
SESSION_REDIS_PORT=6379
SESSION_REDIS_DB=0
```

## Install dependencies

Pipenv is required to install dependencies. Create a virtual environment and install all the dependencies running this command:
```
pipenv install --dev
pipenv shell
```

## Webhooks local server

Execute `flask --help` to see flask server details, by default, you can start the development server with:
```
flask run
```

## Run tests

The directory `tests` contains all the tests cases. Run `pytest` to apply all the defined test cases
```
pytest
```

## Tests coverage report

Check the test coverage running the  `coverage` command.
```
coverage run --source . -m pytest -s && coverage html
```

Then, open the `htmlcov/index.html` file to see the coverage reports.
