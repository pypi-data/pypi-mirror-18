# Lemmes
Compact interface for Assisted Machine Learning, entity extraction & performance test with multilingual support, build in python.

## Install
After clone this repo

    python setup.py build && python setup.py install
    python -m lemmes.download

## Basic Usage

    # see test.py

## Developer Stage
### Pre-Install

 - Docker 1.*

### Run

    cd /[project_path]
    docker build -t lemmes .
    docker run -v $(pwd):/lemmes:rw -it lemmes bash
    python -m lemmes.download

### Test

    invoke test

### Work in

    docker run -v $(pwd):/lemmes:rw -it lemmes bash
