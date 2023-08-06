# Brink Framework

[![Build Status](https://travis-ci.org/lohmander/brink.svg?branch=feature%2Fmodel-rewrite)](https://travis-ci.org/lohmander/brink)

## Installation

    $ pip install brink

## Getting started

Getting started is very easy assuming you have Docker installed.

Start RethinkDB like so

    $ docker run rethinkdb -p 8080:8080 -p 28015:28015 -d --name rethink

And then get started with your project like so

    $ brink start-project myproject
    $ cd myproject
    $ brink sync-db
    $ brink run

## Documentation

Full documentation is (will be) available at <https://lohmander.github.io/brink/>.



