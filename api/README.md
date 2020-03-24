# NT: BACKEND
NT Client Repo can be found here: [ hyperlink to be put here ]


db sytnax:
DATABASE_URL=postgres://{user}:{password}@{hostname}:{port}/{database-name}



## TO DOs

### HTTPS
[https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https]

### TESTS
Get initial tests from here:
* [https://realpython.com/token-based-authentication-with-flask/#blacklist]
* [https://github.com/olibre/flask-restplus-boilerplate/blob/olibre/api/main]
* [https://github.com/miguelgrinberg/flasky]
* [https://github.com/olawalejarvis/blog_api_tutorial/blob/develop/src/views/UserView.py]


### Namespaces
1. Modules --> Amazon --> Data
	* background jobs _redis queue_? _frequency:_ daily | _ideas from here: [https://realpython.com/flask-by-example-implementing-a-redis-task-queue/]
		* transactions, etc.

2. Modules --> Amazon --> Services --> Dashboard
	* entity
	*

3. Modules --> Amazon --> Services --> VAT
	* VAT model
	* background jobs _redis queue_? _frequency:_ daily
		* exchange rate

4. Modules --> Amazon --> (billing)

### Other things
* Mail
    * ~~Registration/Confirmation~~
    * Forgot Password | _ideas from here_: [https://github.com/miguelgrinberg/flasky]
* Decorators
    * eg. ~~admin~~, rate limit | _ideas from here_: [http://pycoder.net/bospy/presentation.html#bonus-material]

### Deployment
* Docker container
* AWS EC2 Cluster, load balancing
--> check out: [https://github.com/Miserlou/Zappa] for *Servless* (however that exactly works)

## API Structure
## Terms (adapted from [flaskerize](http://alanpryorjr.com/2019-05-20-flask-api-example/))
* __Entity__: An entity is a combination of a *data transfer object (dto) schema*, *type-annotated interface*, *SQLAlchemy model*, *Flask controller*, and *CRUD service*.

```
path
└── to
    └── my
        └── doodad
            ├── __init__.py
            ├── controller.py
            ├── controller_test.py
            ├── interface.py
            ├── interface_test.py
            ├── model.py
            ├── model_test.py
            ├── schema.py
            ├── schema_test.py
            ├── service.py
            └── service_test.py

```


## Configurations
* Development
* Testing
* Staging
* Production

*POSTGRES* databases are used for each config.

## Usage

### Seeding the database

```
python manage.py fake_users_db

python manage.py initial_users_db
```

### Running the app

`python wsgi.py`

### Running tests

*open issue*
