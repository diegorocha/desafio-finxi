#!/bin/bash

coverage run manage.py test && coverage html -d htmlcov/
