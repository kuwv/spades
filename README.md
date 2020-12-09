# spades

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://spdx.org/licenses/Apache-2.0)
[![Build Status](https://travis-ci.org/kuwv/python-spades.svg?branch=master)](https://travis-ci.org/kuwv/python-spades)
[![codecov](https://codecov.io/gh/kuwv/python-spades/branch/master/graph/badge.svg)](https://codecov.io/gh/kuwv/python-spades)

## Overview

SWE-681 Final Project - Spades

## Prerequisites

- libevent (MacOS `brew install libevent`)
- Docker
- docker-compose
- mkcert
- Python 3.9

## Install

```
pip install pipenv
pipenv shell
pipenv install --dev
```

## Manual Install

...

```
gunicorn app:app --bind=0.0.0.0:8080 --reload --worker-class=gevent
```

## Credits

Chris Aguilar for Vector Playing Cards
Richard Schneider for cardJS
