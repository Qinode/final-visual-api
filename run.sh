#!/bin/bash

set -e

cd /api
gunicorn -c /api/config/gunicorn.py api:app
