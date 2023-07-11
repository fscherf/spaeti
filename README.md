# Spaeti

![license MIT](https://img.shields.io/pypi/l/spaeti.svg)
![Python Version](https://img.shields.io/pypi/pyversions/spaeti.svg)
![Latest Version](https://img.shields.io/pypi/v/spaeti.svg)

Spaeti is a re-implementation of [prepaid-mate](https://github.com/freieslabor/prepaid-mate).


## Initial Setup

1. Setup [docker](https://www.docker.com/) on your system.

```
$ sudo apt install docker.io docker-compose
$ sudo adduser $USER docker
```

2. Create an environment file from the example environment file and start the app

```
$ cp example.env .env
$ docker-compose up
```

3. While the app is running, setup a database and a admin user

```
$ docker-compose exec app ./docker-entrypoint.sh migrate
$ docker-compose exec app ./docker-entrypoint.sh createsuperuser
```


## Start the App

```
$ docker-compose up
```

All operational configuration is done in `.env`.

Spaeti stores all data in `data/`, which can be reset by running `sudo rm data -rf`.


## Run Tests

### Tests

```
$ docker-compose run playwright tox
```

### Linter

```
$ docker-compose run playwright tox -e lint
```


## Deployment

Before deployment, make sure you changed all sensible configuration in `.env`.

```
$ docker-compose up -d
```
